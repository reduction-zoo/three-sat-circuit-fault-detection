# Campaign state

Budget: 20 rounds. Used: 1.
Board source: 4c2dee3448402208379b169663647146233f04ee.

Capability probe (2026-09-25 UTC): Python 3.12.14 (`/Users/xiweipan/.local/bin/python3`), uv 0.12.17 (`/Users/xiweipan/.local/bin/uv`), Z3 executable and Python binding 5.1.0 (`/opt/homebrew/bin/z3`, locked `z3-solver` 5.1.0.0), Typst 0.15.1 (`/opt/homebrew/bin/typst`), Lean 4.34.1 and Lake 5.0.0 (`/opt/homebrew/bin/lean`, `/opt/homebrew/bin/lake`). Mathlib availability is unconfirmed. The required technical-writing skill and registered Codex reviewer are present. No formalization was requested.

Prepare: 115 fixed legal source cases (100 seeded random, 15 edges); Z3 source oracle and independent exhaustive target oracle; self-test passed on 2026-09-25. See [preparation](work/preparation.md). No candidate exists yet.

Current claim: complete explicit reconstruction, pending independent review and paper. Correctness evidence: general proof plus 115 prepared and 123 separate verified instances; novelty: classical mechanism; significance: meets fixed reconstruction question. Uncalibrated prospects of a reviewable reconstruction within the remaining budget: high, based on the direct proof and finite checks; earlier assessment: none.

Next action: follow-up independent review of round 001 same-strategy repair.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | `z AND φ` as designated output | Prepared end-to-end candidate loop | Passed 115 prepared instances/201 outputs and 123 additional instances/243 outputs; review 001 revise, local repair rechecked | [round](rounds/001/round.md), [verification](work/verification.md), [review](reviews/001/review.md) |
