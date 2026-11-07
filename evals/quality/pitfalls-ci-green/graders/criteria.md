---
type: llm
---

PASS if the reply says not to trust "green" without opening the latest run of every required job, checks the runtime version is the same in .nvmrc, engines, CI and Dockerfiles, asks whether CI is a required check on main, and says to prove each gate can fail by breaking it on a throwaway branch.
FAIL if it accepts that CI is green and only suggests code review or more tests.
