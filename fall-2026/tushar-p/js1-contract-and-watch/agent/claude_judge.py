"""The Claude judge. Its verdicts are model judgment, never a record.

Claude receives only the persona's rule fields, the posting's title, location, dates and
HTML-stripped content, and R1–R6 in plain language. Model fallback is off: the request
sends no fallback parameter, so the model that answers is the configured one.
"""

import json
from datetime import date
from pathlib import Path

from .allowlist import check_url
from .errors import ValidationError
from .persona import RULE_FIELDS
from .validator import POSTING_FIELDS, VERDICTS, validate_claude_reply

CLAUDE_LABEL = "model judgment"

SYSTEM_PROMPT = """\
You judge whether one job posting is relevant to one job seeker. You receive the
seeker's rule fields from their résumé, one posting, and the run date.

Apply these six checks. Each check is pass, fail, or unknown. Matching is whole-word
and case-insensitive unless a check says otherwise.

R1 Title. Pass if the title contains one of job_search.target_titles. Fail if it
contains none. Fail if it contains Senior, Staff, Principal, Lead, Manager, or Intern;
these words win over target titles. "Internal" and "Internship" are not "Intern", and
"Software Engineering" is not "Software Engineer".

R2 Freshness. The posting date is first_published, or updated_at if that is missing,
taken as a calendar date in America/New_York. 21 days or fewer before the run date:
pass. 22 or more: fail. A future date: pass. Both dates missing: unknown.

R3 Location. job_search.work_country is US. Pass if location.name shows the US: "United
States", "USA", "U.S.", uppercase "US" (also in forms like "US-Remote"); the cities San
Francisco, South San Francisco, New York, New York City, Seattle, Chicago, Atlanta; the
short forms SF, NYC, NY, SEA, CHI, ATL, DC; a US state name; or an uppercase US state
abbreviation directly after a comma or semicolon (", WA"), except "CA", which on this
board means Canada. One US match among several locations is enough. Unknown if the whole
value is only "Remote" or a placeholder ("N/A", "na", "LOCATION", empty). Otherwise fail.

R4 Experience. job_search.years_experience is 0, so the seeker is a new grad (0–3
years). Find every "N+ years" and every "N–M years" (also "N-M" and "N to M") in the
content; each one's minimum is N. Take the largest of those minimums: 3 or less is pass,
more than 3 is fail. No matches: unknown. Plain "N years" and spelled-out numbers do not
count.

R5 Sponsorship. job_search.needs_sponsorship is true. Fail if the content contains
"unable to sponsor", "will not sponsor", "does not sponsor", "no sponsorship", "without
sponsorship", or "without the need for sponsorship". Otherwise pass.

R6 Skills. Pass if at least one item in skills appears as a whole word in the content
("Java" does not match "JavaScript"). Otherwise fail.

Verdict: any check fails -> not_relevant. Otherwise any check unknown -> cannot_tell.
Otherwise -> relevant.

Reply with one JSON object and nothing else:
{"posting_id": "<the posting_id you were given, as a string>",
 "verdict": "relevant" | "not_relevant" | "cannot_tell",
 "justification": [{"resume_field": "...", "posting_field": "...", "evidence": "..."}]}

Every justification entry must name the résumé field and the posting field it relies on.
resume_field must be one of: """ + ", ".join(RULE_FIELDS) + """.
posting_field must be one of: """ + ", ".join(POSTING_FIELDS) + """.
evidence quotes or states the value you found. Use no other keys.
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "posting_id": {"type": "string"},
        "verdict": {"type": "string", "enum": list(VERDICTS)},
        "justification": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "resume_field": {"type": "string", "enum": list(RULE_FIELDS)},
                    "posting_field": {"type": "string", "enum": list(POSTING_FIELDS)},
                    "evidence": {"type": "string"},
                },
                "required": ["resume_field", "posting_field", "evidence"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["posting_id", "verdict", "justification"],
    "additionalProperties": False,
}


def build_request(posting: dict, content_text: str, fields: dict, run_date: date,
                  model: str, max_tokens: int) -> dict:
    """Keyword arguments for messages.create. `fields` holds only the five rule fields."""
    payload = {
        "run_date": run_date.isoformat(),
        "resume_rule_fields": {key: fields[key] for key in RULE_FIELDS},
        "posting": {
            "posting_id": str(posting["id"]),
            "title": posting.get("title"),
            "location.name": (posting.get("location") or {}).get("name"),
            "first_published": posting.get("first_published"),
            "updated_at": posting.get("updated_at"),
            "content": content_text,
        },
    }
    return {
        "model": model,
        "max_tokens": max_tokens,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False, indent=2)}],
        "output_config": {"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
    }


def make_client(api_key: str, base_url: str):
    """Anthropic client pinned to an allow-listed base URL (ANTHROPIC_BASE_URL is not used)."""
    check_url(base_url)
    import anthropic  # imported here so --no-claude runs and tests never need the SDK

    return anthropic.Anthropic(api_key=api_key, base_url=base_url)


def _invalid(reason: str, model, reply_path: Path) -> dict:
    return {
        "claude_verdict": None,
        "claude_justification": None,
        "claude_valid": False,
        "claude_model": model,
        "claude_invalid_reason": reason,
        "claude_reply_path": str(reply_path),
        "claude_label": CLAUDE_LABEL,
    }


def _dump(response) -> str:
    if hasattr(response, "model_dump_json"):
        return response.model_dump_json(indent=2)
    return repr(response)


def judge(client, request: dict, posting_id, reply_path: Path) -> dict:
    """Call Claude once, save the raw reply, and validate it. Invalid output is never repaired."""
    reply_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = client.messages.create(**request)
    except Exception as err:  # any API or network failure leaves nothing to validate
        status = getattr(err, "status_code", None)
        reason = f"API call failed: {type(err).__name__}" + (f" (HTTP {status})" if status else "")
        reply_path.write_text(reason + "\n", encoding="utf-8")
        return _invalid(reason, None, reply_path)

    reply_path.write_text(_dump(response), encoding="utf-8")
    model = getattr(response, "model", None)
    if getattr(response, "stop_reason", None) == "refusal":
        return _invalid("refusal", model, reply_path)
    text = next((b.text for b in (response.content or []) if getattr(b, "type", None) == "text"), None)
    try:
        data = validate_claude_reply(text, posting_id)
    except ValidationError as err:
        return _invalid(str(err), model, reply_path)
    return {
        "claude_verdict": data["verdict"],
        "claude_justification": data["justification"],
        "claude_valid": True,
        "claude_model": model,
        "claude_invalid_reason": None,
        "claude_reply_path": str(reply_path),
        "claude_label": CLAUDE_LABEL,
    }
