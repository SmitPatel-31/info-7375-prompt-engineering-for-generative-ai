# Hand-labeling rule

## Executive summary

This is the rule Smit Patel used to hand-label 20 real Airbnb postings as worth (or not
worth) a day of the fictional candidate's time. It was chosen on 2026-10-24, before any
posting was labeled and before any prompt was run. The labels it produced are the answer
key for the sampling report and the prompt experiment. It is a human judgment rule, and it
is deliberately not the same as the agent's rule in CONTRACT.md. The agent's rule never
looks at location or years of experience, and part of the point is to see what that costs.

## The rule

A posting is **RELEVANT** to Aarav Patel (fictional F-1 STEM OPT new-grad backend/platform
engineer in Boston, open to remote) if and only if **all** hold:

1. It is an individual-contributor engineering role, not a manager role.
2. The title is not Senior, Staff, or Principal.
3. The experience it requires is 5 years or less.
4. The location is in the United States or remote-US. OPT work has to be in the US.

Otherwise it is **NOT RELEVANT**.

Chosen by Smit Patel, 2026-10-24, from options Claude offered in the build session (the
"IC + early-career + US" option).
