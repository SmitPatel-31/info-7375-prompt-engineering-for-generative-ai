# CONTRACT — Job-Search Agent 1

Version 0.1 · 2026-10-27 · Tushar Patel

Scope: one Greenhouse board, one fictional persona résumé, new postings only, every verdict justified.

## In

- **Board:** host `boards-api.greenhouse.io`, board token `stripe`.
  Endpoint: `https://boards-api.greenhouse.io/v1/boards/stripe/jobs?content=true`
  (`content=true` is needed so the posting text is available for rules R4–R6.)
- **Résumé:** fictional persona Cole Palmer, `persona/cole-palmer.example.json` (invented for this assignment; 555 phone, `@example.com` email).
- **Résumé fields the rule reads** (no others):

  | Rule input | Persona JSON key |
  |---|---|
  | target titles | `job_search.target_titles` |
  | skills | `skills` |
  | years of experience | `job_search.years_experience` |
  | work location | `job_search.work_country` |
  | needs sponsorship | `job_search.needs_sponsorship` |

- `personal` (name, location, phone, email), `education`, and `experience` are never read by the rule, and contact fields are never printed.
- If any required résumé field is missing, the agent **stops with an error** and produces no verdicts.
- **State file:** the list of posting ids already seen, kept in the project folder.

## Out

For each **new** posting (id not in the state file), one record:

- `posting_id`, `title`, `url`, `location`, `date_used` (which date field, and its value)
- `rule_verdict`: `relevant` | `not_relevant` | `cannot_tell` — labeled **record** (anyone can recompute it)
- `rule_justification`: one entry per check R1–R6, each naming the **résumé field**, the **posting field**, the value found, and the result (pass / fail / unknown)
- `claude_verdict` + `claude_justification` — labeled **model judgment**, in a fixed JSON format. A validator rejects any Claude output that does not match the format.

Per run: run date, number of postings fetched, number new, path to the saved raw response.

The **first run is a baseline**: it records all ids and reports **0 new**.

## Refuses

- Fetching any host not on the allow-list. Allow-list: `boards-api.greenhouse.io` (plus the Claude API for the judgment step).
- Showing a real résumé on screen or on GitHub. Only the fictional persona is used.
- Presenting Claude's judgment as a fact. Claude verdicts are always labeled model judgment.
- Applying, emailing, messaging, or logging in anywhere.

## The rule

Each check returns **pass**, **fail**, or **unknown**. All matching is case-insensitive.

- **R1 Title.** Pass if the posting `title` contains one of `job_search.target_titles` ("Software Engineer", "AI Engineer", "Backend Engineer"). Fail if it contains none, or if it contains Senior, Staff, Principal, Lead, Manager, or Intern.
- **R2 Freshness.** The posting date is `first_published`; if that is missing, `updated_at`. Fail if it is more than **21 days** before the run date. Otherwise pass.
- **R3 Location.** Compared with `job_search.work_country` (US). Pass if the posting `location.name` clearly shows the US: a US state name or abbreviation, "United States", "US", or "USA". Remote and hybrid are OK when they show the US. Unknown if it is only "Remote". Fail for everything else (for example, plain "Dublin").
- **R4 Experience.** New grad means 0–3 years (`job_search.years_experience` is 0). Find "N+ years" or "N–M years" in the posting text. Pass if the minimum N is 3 or less. Fail if it is more than 3. Unknown if no years are stated.
- **R5 Sponsorship.** Applies because `job_search.needs_sponsorship` is true. Fail if the posting text says it will not sponsor (e.g. "unable to sponsor", "will not sponsor", "does not sponsor", "no sponsorship", "without the need for sponsorship"). If the posting says nothing about sponsorship, pass.
- **R6 Skills.** Pass if at least **1** item in `skills` appears as a whole word in the posting text. Fail if none do.

**Verdict:**
1. Any check fails → `not_relevant`.
2. Otherwise, any check unknown → `cannot_tell` (a person decides).
3. Otherwise → `relevant`.

## Wrong versions (tests must catch these)

1. **A justification that cites no fields.** Test: a verdict whose justification entries lack a résumé field or a posting field is rejected.
2. **An already-seen posting reported as new again.** Test: running twice on the same saved raw response reports 0 new on the second run.

## What a failure looks like

2026-10-27: The agent fails if it marks as relevant a posting dated more than 21 days before the run, a posting requiring more than 3 years of experience, a posting outside the US, or a posting that says it will not sponsor visas.
