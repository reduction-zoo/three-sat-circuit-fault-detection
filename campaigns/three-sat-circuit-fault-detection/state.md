# Campaign state

Budget: 20 rounds. Used: 1.
Board source: 4c2dee3448402208379b169663647146233f04ee.

Capability probe (2026-09-25 UTC): Python 3.12.14 (`/Users/xiweipan/.local/bin/python3`), uv 0.12.17 (`/Users/xiweipan/.local/bin/uv`), Z3 executable and Python binding 5.1.0 (`/opt/homebrew/bin/z3`, locked `z3-solver` 5.1.0.0), Typst 0.15.1 (`/opt/homebrew/bin/typst`), Lean 4.34.1 and Lake 5.0.0 (`/opt/homebrew/bin/lean`, `/opt/homebrew/bin/lake`). Mathlib availability is unconfirmed. The required technical-writing skill and registered Codex reviewer are present. No formalization was requested.

Prepare: 115 fixed legal source cases (100 seeded random, 15 edges); Z3 source oracle and independent exhaustive target oracle; self-test passed on 2026-09-25 before construction. See [preparation](work/preparation.md).

Status: `ready_for_expert_review` (agent assessment, not human certification). Current claim: complete explicit reconstruction. Correctness evidence: general proof, 115 prepared and 123 separate verified instances, large-count CLI checks, and independent advance review 002. Novelty: classical mechanism; significance: meets fixed reconstruction question. A three-page Typst PDF was compiled and visually inspected page by page. Formalization and expert certification remain pending. Uncalibrated prospects of a reviewable reconstruction within the remaining budget: high, based on the direct proof and finite checks; earlier assessment: none.

Research model provenance (checked for publication on 2026-09-25): the original Codex session log records `gpt-6-sol` in the research turn context at 10:55:16 UTC and the continuation at 11:48:29 UTC. The current default is also `gpt-6-sol`; the historical session contexts, rather than that default, support the attribution. The reviewer-specific backend variant was not exposed.

Next action: expert review of the reconstruction and its encoding assumptions. No new research round is needed under the fixed acceptance criteria.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | `z AND φ` as designated output | Prepared end-to-end candidate loop | Complete reconstruction; review 001 revise, local repair, review 002 advance; paper inspected | [round](rounds/001/round.md), [verification](work/verification.md), [reviews](reviews/002/review.md), [paper](work/manuscript.pdf) |
