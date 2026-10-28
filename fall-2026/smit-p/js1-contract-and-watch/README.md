# Job-Search Agent 1 — The Contract and the Watch

**Smit Patel · INFO 7375 · Fall 2026 · Chapters 1–3**

## Executive summary

This is the first layer of a job-search agent. It watches Airbnb's public job board,
remembers which postings it has already seen, and reports only the new ones. For each
new posting it gives two verdicts on whether the job fits a fictional candidate's
résumé. One comes from a written rule that anyone can recompute by hand. The other comes
from Claude and is always labeled as a model's judgment. Every verdict names the résumé
fields and posting text behind it.

What it found on 2026-10-24: Airbnb had 191 postings, and only 3 fit the candidate under
the written rule. The more useful finding is a gap in my own contract. The rule ignores
location, so it calls Software Engineer jobs in Brazil "relevant" for a US student on OPT.
Claude made the same mistake, identically, every time it was asked. Repeatable is not the
same as right. A prompt revision that adds a US-location condition fixed the verdicts but
broke the output format, because the format has nowhere to cite a location. That bug is
still open. Fetching and state stay in tested code; Claude only judges text it is
handed.

## Run record

| | |
|---|---|
| Language | Python 3.10+ (tested on 3.12.7), **standard library only**, no `pip install` |
| Claude judge | Claude Code CLI (`claude`, tested 2.1.305), signed in. Only needed for `--claude` and `experiments/` |
| Board | Greenhouse `airbnb`; allow-list = `boards-api.greenhouse.io` only |
| Persona | Aarav Patel (fictional, `@example.com`, `555` phone), `persona/aarav-patel.resume.json` |
| Judge model | `claude-sonnet-5-5` (CLI alias `sonnet`) |

## Commands (run from this folder, on a fresh clone)

```bash
python3 -m unittest discover -s tests -v
```

```bash
python3 src/watch.py --board airbnb --resume persona/aarav-patel.resume.json --state runs/state.json --out runs/ --label live --claude
```

The first command runs the 24 contract tests, offline. The second is the watch. On a
fresh state file it is a baseline and reports nothing. Run it again on another day and
it reports only the postings that appeared in between.

Re-run the seeded pair (no network; reproduces `runs/seeded/`):

```bash
python3 src/watch.py --board airbnb --resume persona/aarav-patel.resume.json --state /tmp/js1-seeded-state.json --out /tmp/js1-seeded --fixture runs/seeded/earlier-snapshot-SEEDED.json --label seeded-baseline
```

```bash
python3 src/watch.py --board airbnb --resume persona/aarav-patel.resume.json --state /tmp/js1-seeded-state.json --out /tmp/js1-seeded --fixture runs/raw-20261024T192545-live.json --label seeded-run2
```

Recompute every number in the reports from the saved results (no network, no Claude):

```bash
python3 experiments/score.py
```

Re-run the Claude experiments (about $1, makes 60 calls):

```bash
python3 experiments/run_claude.py --set sampling --prompt baseline --repeats 4 --out experiments/results/rerun-sampling.jsonl
```

(`--set dev|held_out`, `--prompt baseline|revision` for the prompt experiment.)

## What ran

| Run | When | Source | Seen | New | Evidence |
|---|---|---|---|---|---|
| Live baseline | 2026-10-24 19:25 ET | `boards-api.greenhouse.io` | 191 | 0 (baseline) | `runs/raw-20261024T192545-live.json`, `runs/state.json`, `runs/report-…-live.md` |
| **Seeded** baseline | 2026-10-24 19:26 | `runs/seeded/earlier-snapshot-SEEDED.json`: the live response with the 10 most recently published postings removed (**synthetic**, labeled in the file) | 181 | 0 (baseline) | `runs/seeded/*seeded-baseline*` |
| **Seeded** run 2 | 2026-10-24 19:26 | the real live response | 191 | **10** (rule: 0 relevant; Claude: 0 relevant, 10/10 replies accepted) | `runs/seeded/*seeded-run2*`, `runs/seeded/state.json` |
| **Live run 2** | 2026-10-28 15:35 ET (run by Smit) | `boards-api.greenhouse.io` | 194 | **17** (14 removed since 10-24; rule: 0 relevant; Claude: 0 relevant, 17/17 replies accepted) | `runs/raw-20261028T153510-live.json`, `runs/run-…-live.json`, `runs/report-20261028T153510-live.md`, `runs/state.json` |

Other evidence: `SAMPLING-REPORT.md`, `PROMPT-EXPERIMENT.md`, `ACTION-SURFACES.md`,
`experiments/` (prompts, labels, raw replies, scores), `DECISIONS.md`, `SOURCES.md`,
`FRICTIONAL.md`.

## Layout

```
CONTRACT.md                 written first (commit c29d163), before any code
src/rule.py                 the written rule + justification validator (a record)
src/claude_judge.py         Claude under a prompt contract + strict reply validator (a judgment)
src/watch.py                allow-listed fetch, raw saved, diff by id, reports
tests/test_contract.py      24 tests incl. both wrong versions; fixtures day1/day2
prompts/                    baseline.md, revision.md (one change)
experiments/                selection, labeling rule, hand labels, run_claude.py, score.py, results/
runs/                       raw responses, state files, run records, reports
```

## Sign-off — Job-Search Agent 1

> **DRAFT by Claude. Not signed.** Smit must read it, correct anything untrue, and then
> sign or withhold it. The "how" column states honestly that Claude wrote the tests.

**Checked**

| Property | Test (`tests/test_contract.py`) or check |
|---|---|
| Rule verdicts match hand-worked answers on 7 fixture postings | `TheRule.test_hand_worked_verdicts` |
| Whole-word matching (Java≠JavaScript, SQL≠PostgreSQL, Go≠Google) | `TheRule.test_whole_word_matching` |
| Wrong version 1 (labels on wrong postings) is caught | `WrongVersion1_*` (3 tests) |
| Wrong version 2 (justification cites nothing / invents a citation) is caught | `WrongVersion2_*` (3 tests) |
| Baseline reports nothing; run 2 reports exactly the added ids; no-change run reports nothing | `TheWatch.*` |
| Failed fetch leaves state untouched; raw saved byte-for-byte | `TheWatch.test_failed_fetch_leaves_state_alone`, `test_raw_response_saved_untouched` |
| Off-list hosts, http, bad slugs, and non-persona résumés refused | `Refuses.*` |
| Claude replies outside the fixed format rejected (10 cases) | `ClaudeReplyValidator.test_rejects_everything_else` |
| The tests notice deliberate bugs | mutation check: 6 of 7 caught after one added test. The 7th removes a guard that a second check already covers (FRICTIONAL F2) |
| Report numbers match the raw results | recomputation, `experiments/score.py` |

**How:** the 20 hand labels were by hand (me). Every test was written by Claude against
CONTRACT.md, right **after** Claude wrote the code, in the same session. So none of them
is an independent test I wrote before reading Claude's code. The numbers in
the reports were checked by recomputation (`score.py`). Two claims in Claude's report
drafts were wrong when re-checked against the data, and were corrected.

**Not checked**

1. Whether "new by id" matches "new job" for a person. On 10-28, 7826337 «Machine
   Learning Engineer, Assistance Engineering» was new by id, but a posting with the same
   title (7716341) was already on the board. I did not check whether it is a different
   role or a duplicate.
2. Whether the hand-worked expected verdicts in the tests are themselves right. Claude
   derived them, and I have not re-derived them by hand.
3. The rule on boards other than Airbnb, on non-Greenhouse boards, or on postings whose
   HTML differs from Airbnb's.
4. Claude's verdict stability at other temperatures, on other models, or on other days.
5. Whether any of the 3 rule-relevant jobs is actually worth applying to (location,
   sponsorship, and years are not in the rule).
6. Behavior when the board is paginated or returns more than one page.

**Not claiming:** that the agent finds good jobs. It applies my written rule, which has a
known location gap. Not claiming that 9/10 means anything with one positive label. Not
claiming that Claude's verdicts are facts. Not claiming that the revision prompt is
better.

**Signed or withheld:** ____________ (name, date)

## Driver's seat

| Part of the task | Claude should | I should | Why it stays mine | Evidence the split happened |
|---|---|---|---|---|
| The contract | offer options, write them up, implement against them | choose board, persona, rule, wrong versions, failure | it defines what "right" means; whoever writes it decides what gets checked | DECISIONS D1–D6; `CONTRACT.md` alone in commit `c29d163` |
| Hand labels | present the facts of each posting | label every posting | the labels are the answer key; if Claude labels, the experiment grades Claude against itself | DECISIONS D8–D11; `56ca4e8` |
| The labeling rule | point out when my labels contradict my rule | decide whether the rule or the labels change | only I know which one I meant | D9–D10: my typed answer contradicted v1, and I chose to amend (LABELING-RULE.md) |
| Code, tests, runs | write and run all of it | read the reports, check the numbers | — | SOURCES.md |
| Is a job worth a day? | flag, cite, sort | decide | that is my time and my visa clock | every report ends at "you decide" |
| Signing | draft | sign or withhold | my name goes on it | the blank line above |
