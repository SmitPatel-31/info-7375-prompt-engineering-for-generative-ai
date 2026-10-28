# FRICTIONAL — what actually happened

## Executive summary

This is an honest log of what went wrong, what was tried, and what is still unresolved
while building Job-Search Agent 1. Everything in the first section happened on
2026-10-24 and traces to a commit, a file, or a test. **The section "In my own words" is
for me (Smit) to write.** A drafted log of events is not the same as my account of them.

## Log of events (drafted by Claude from the session; each item is traceable)

| # | What happened | What was done | Accepted / modified / rejected | Trace |
|---|---|---|---|---|
| F1 | My first answer named only one wrong version; the assignment needs two | asked again; I picked "Empty justification" | accepted | DECISIONS D4–D5, `c29d163` |
| F2 | All 23 tests passed on the first run. That can mean the tests are too weak | Claude deliberately broke the code 7 ways. 5 were caught. Removing the posting-id check (M2) was **not** caught: shifted labels only failed because quotes happened not to match | a direct test was added (`test_verdict_checked_against_another_posting_rejected`) and M2 is now caught. M1 (empty-citation guard removed) is still "not caught", because a second check in the validator covers it | `tests/test_contract.py` |
| F3 | The first random 20-posting sample had 19/20 senior titles, so labels would be almost all "no" and the experiment useless | redrawn, stratified by seniority, before any labeling. The old draw is kept | Claude's decision, not mine. Check it | `experiments/selection-v1-degenerate.json`, `783402f` |
| F4 | Airbnb has only 6 non-senior engineering postings (of 52) | all 6 used. Labels still ended at 1 relevant / 19 not | unresolved: the board is a poor fit for a new-grad persona | `experiments/selection.json` |
| F5 | While labeling held-out, I typed a narrower rule than the one I had committed (SWE/Cloud/Full-Stack, ≤3–4 yrs). It contradicted v1 on «Operations Engineer» | asked to choose. I amended the rule to v2 rather than relabel. The amendment is in the file, not overwritten | modified (my rule) | `experiments/LABELING-RULE.md`, `56ca4e8` |
| F6 | One label (8274152) came back with "No preference" | asked again; "Relevant" | — | DECISIONS D11 |
| F7 | The baseline prompt and the **written rule** both call Brazil postings relevant. The contract has no location check | the revision prompt adds one. The **rule in CONTRACT.md is not changed**, because a contract edited after running is not "written first" | unresolved: the agent's rule still ignores location | PROMPT-EXPERIMENT.md |
| F8 | The revision fixed the verdicts but 3 replies were rejected: Claude quoted the location, which the output format cannot hold | not fixed. It would be a second change in a one-change experiment | the next layer should add a `location` evidence field | `experiments/results/dev-revision.jsonl`, `heldout-revision.jsonl` |
| F9 | 1 of 20 sampling replies cited `devops_cicd[0]` (missing `skills.`) | rejected by the validator, counted as a fail | accepted the strictness | `sampling-baseline.jsonl` |
| F10 | The agent with fetch/write tools fetched without `content=true`, had 5 commands denied, and returned a wrong but well-formed verdict that **passed the validator** | kept as evidence. The validator checks conformance, not adequacy | it informed the autonomy choice | ACTION-SURFACES.md |
| F11 | A shell `echo ===DEV` line broke under zsh and stopped a chained command | re-ran the second command on its own | — | none (session only) |
| F12 | A real second calendar day is not possible on day 1 | ran a clearly labeled seeded pair (an "earlier" snapshot built by removing the 10 newest postings) and left the live day-2 command in the README | done 2026-10-28 by Smit: 194 seen, 17 new, 14 removed, 0 relevant by either judge | `runs/seeded/`, `runs/*20261028T153510*` |
| F13 | Day-2 output in the terminal showed `&amp;` in titles, which looked like an escaping bug | checked the saved raw response: titles hold a plain `&`; the `&amp;` came from how the output was displayed, not from the agent | no change | `runs/raw-20261028T153510-live.json` |
| F14 | 7826337 was reported new, but a posting with the same title (7716341) was already on the board | correct under the contract (new = new id). Whether it is a duplicate is not checked | unresolved, added to "Not checked" | `runs/run-*20261028*` |

## In my own words (Smit — to write)

- What surprised me:
- What I checked myself, and how:
- What I would not have caught without the tests or the hand labels:
- What I disagree with in the drafts above:
