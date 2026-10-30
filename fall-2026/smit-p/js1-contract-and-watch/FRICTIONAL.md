# FRICTIONAL — what actually happened

## Executive summary

This is an honest log of what went wrong, what was tried, and what is still unresolved
while building Job-Search Agent 1. F1–F11 happened on 2026-10-24. F12–F25 were added on
2026-10-28. Each one traces to a commit, a file, or a test. The last section holds my own
answers, selected by me from statements Claude offered. A drafted log of events is not
the same as my account of them.

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

### 2026-10-28: a TA-style review before submitting

Smit asked for every rubric line to be checked, after losing marks on an earlier
assignment. A separate Claude reviewer (a subagent given only the brief and this folder)
graded it and reported 15 issues. Each was checked against the files before acting.

| # | Found | Done | Trace |
|---|---|---|---|
| F15 | The course folder rule says "no full names", and the files used my full name | replaced with "Smit P." in 6 files, **including one line of CONTRACT.md**, which is recorded in its errata | `git diff c29d163 -- CONTRACT.md` |
| F16 | Three held-out labels were **inferred by Claude** from a rule I typed, while `labels.json` said "Claude did not choose them" | I labeled them explicitly (all not relevant, unchanged), and a correction was added to the file instead of rewriting it | DECISIONS D12, `labels.json` `_provenance_correction` |
| F17 | PROMPT-EXPERIMENT said the revision came "after reading the development results". The timestamps show it was chosen 13 s after them, by Claude, and the Brazil miss had already appeared in sampling. Claude had also seen the held-out titles during selection | the report now says so, as a limitation | `experiments/results/*.jsonl` `asked_at` |
| F18 | ACTION-SURFACES blamed the agent for all 5 denials. The 5th was a plain, correct fetch, blocked because the permission pattern did not match a quoted URL | rewritten to describe each denial as it happened | `surface3-result.json` |
| F19 | 7 of 17 day-2 records name `claude-haiku-5-5`, because the code saved only the first model the CLI listed | the code now saves all (`models_used`). The day-2 record is **not** edited; it is explained in README | `src/claude_judge.py`, `runs/run-20261028T153510-live.json` |
| F20 | Tests for wrong version 1 were weak: one only asked "caught > 0", and one could never fail | now every shifted label must be caught, plus a same-title-twin test and an end-to-end test through `watch.py`. The never-fail test was removed | `tests/test_contract.py` |
| F21 | The "7 mutants, 6 caught" claim had no file behind it | added `tests/mutation_check.py` (13 mutants), which writes `tests/mutation-log.md`: 12/13 caught | `tests/mutation-log.md` |
| F22 | The validators accepted part-word quotes (Java in JavaScript), whole résumé sections as "fields", and crashed the watch on a failed Claude call | fixed. All 87 saved Claude replies were re-validated: no outcome changed | CONTRACT.md errata 3 |
| F23 | Small mismatches between contract text and code (state file shape, validator strictness), a constructed example not labeled as such, and selection-method text that does not match what ran | listed in CONTRACT.md errata and in a `selection.json` erratum. The original text is not rewritten | CONTRACT.md, `selection.json` |
| F24 | Reports said "I asked / I gave" for steps Claude ran | corrected, and an authorship line added to each report | the three report files |
| F25 | After the hand-check test was added, the mutation check suddenly reported **13/13 caught**. The test should still have let M1 survive, so the number was suspicious. Cause: the harness copied `src/ tests/ persona/` but not `hand-check/`, so the new test *errored* on every mutant, and each error was counted as "caught". A false 100% | the harness now copies everything the tests read, and refuses to run unless an **unmutated** copy passes first. Result back to 12/13, which is honest | `tests/mutation_check.py` (`copy_tree`, sanity check) |
| F26 | 2026-10-30: the hand check was meant to be mine. I asked Claude to fill in `hand-check/predictions.json` instead. Claude also found that the test command it had given me (`tests.test_hand_check`) failed, because `tests/` is not a package | Claude wrote the predictions from the posting text, labeled `by: Claude`, before running the test: 2/2 OK. README, SOURCES, and the test file say who wrote them. The command was corrected to `discover -p` | so the code has no independent check by me | `hand-check/predictions.json` |
| — | **Not fixed:** the rule still has no location check. Dev has 0 positive labels. No test was written by me before reading Claude's code | stated in README "Not checked" / PROMPT-EXPERIMENT limits | — |

## My answers (selected by Smit from statements Claude offered, 2026-10-30)

I asked Claude to write this section. It would not put words in my mouth, so it offered
statements and I picked the ones that are true for me. These are my selections; the
sentences are Claude's wording.

- **What surprised me:**
  - Claude called the São Paulo job relevant every single time it was asked: repeatable, but wrong.
  - Airbnb had almost no new-grad software roles, so the board was a poor fit for the persona.
  - All tests passed first time, and only deliberately breaking the code showed some were too weak.
- **What I checked myself:**
  - I read and labeled the 20 sample postings myself.
  - I ran the live watch on Oct 28 and saw 17 new postings, 0 relevant.
  - I ran the full test suite on Oct 28 and saw it pass.
- **What I would not have caught without the tests or the hand labels:**
  - Without my labels I would not have seen that the rule calls Brazil jobs relevant for a US OPT student.
  - Without the mutation check I would have trusted tests that could not fail.
- **What I disagree with in the drafts above:** I don't disagree with anything in the drafts.
- **Not selected** (offered, but not true for me or not chosen): that the fetch-tool agent's
  confident wrong answer surprised me; that I read the three reports; that I would have
  trusted Claude's verdicts for being fluent; that I would have believed the false 13/13.
