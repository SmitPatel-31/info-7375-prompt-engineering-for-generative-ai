# SOURCES

## Executive summary

This file says where each part of this assignment came from: what I reused, what I
decided and wrote, and what Claude (Claude Code, model Opus 5.5) produced. In short:
Claude wrote all of the code and the first drafts of every document. I made the
decisions the grade depends on: the contract's choices, the labeling rule, and all 20
hand labels. The fetch-and-diff design is adapted from *The Reallocation Engine*.

## Used (not written for this assignment)

| Source | What I used |
|---|---|
| *The Reallocation Engine* (github.com/nikbearbrown/the-reallocation-engine), `search/examples/aarav-patel/resume.example.json` | the fictional persona résumé, copied unchanged into `persona/` |
| *The Reallocation Engine*, `.claude/skills/greenhouse-watch/` | the design of allow-listed fetch → raw response saved → diff by id → baseline first run → state written last. `src/watch.py` is a new, smaller implementation of that design and copies no code |
| Greenhouse Job Board API, `https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true` | the live data (fetched 2026-10-24) |
| Course Chapters 1–3 and the assignment brief | the structure of the three reports and the sign-off |
| Python 3.12 standard library; Claude Code CLI 2.1.305 | toolchain |

## Decided and written by me (Smit P.)

- Every choice in CONTRACT.md: board, persona, relevance rule, both wrong versions, and
  the failure sentence (DECISIONS.md D1–D6). Claude wrote them up as prose.
- The hand-labeling rule and its amendment (D7, D10).
- All 20 hand labels (D8, D9, D11). Three of them were first inferred by Claude from a
  rule I typed, then labeled explicitly by me on 2026-10-28 (D12).
- The live day-2 run, 2026-10-28 (D14).
- Review, correction, and signature of the sign-off in README.md. **Not done yet: see
  README.**
- The hand-check predictions were **not** written by me. Claude wrote them at my request
  on 2026-10-30 (`hand-check/predictions.json`, field `by`).
- My answers in FRICTIONAL.md (selected by me from statements Claude offered, 2026-10-30).

## Contributed by Claude (Claude Code, Opus 5.5, session of 2026-10-24)

- All code: `src/rule.py`, `src/watch.py`, `src/claude_judge.py`, `experiments/run_claude.py`,
  `experiments/score.py`.
- All tests, `tests/test_contract.py`, and the two test fixtures. The expected verdicts
  in the tests were worked out by Claude by hand from CONTRACT.md. I have not
  independently re-derived them.
- Both prompt contracts in `prompts/`, including the choice of the one revision.
- The mutation check (`tests/mutation_check.py`, deliberately breaking the code to confirm the tests notice).
- A TA-style review on 2026-10-28 by a separate Claude subagent that saw only the brief
  and this folder. Its 15 findings, and what was done with each, are in FRICTIONAL.md
  F15–F24.
- Running every live fetch, seeded run, and the 60 + 3 Claude calls.
- First drafts of README.md, SAMPLING-REPORT.md, PROMPT-EXPERIMENT.md,
  ACTION-SURFACES.md, DECISIONS.md, this file, and the FRICTIONAL.md draft.
- The model answering inside the experiments was `claude-sonnet-5-5`. Its replies are
  data (`experiments/results/*.jsonl`), not authorship.
