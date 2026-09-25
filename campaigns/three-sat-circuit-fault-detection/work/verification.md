# Verification evidence

Candidate: [`algorithm.py`](algorithm.py), gated-formula construction and recovery, checked 2026-09-25. Run from repository root after `uv sync --locked`:

```sh
uv run python campaigns/three-sat-circuit-fault-detection/work/check.py --self-test
uv run python campaigns/three-sat-circuit-fault-detection/work/check.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py
uv run python campaigns/three-sat-circuit-fault-detection/work/verify.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py
```

Observed prepared loop: 115 instances, 201 independently generated valid target outputs, 87 target-feasible and 28 target-`NO-SOLUTION` instances. Each map and extraction ran in a fresh subprocess; target input vectors were exhaustively enumerated (at most seven inputs). The second script imports neither the candidate nor the prepared checker. It exhausts all one-variable formulae of zero, one or two ordered three-literal clauses (73) and checks 50 additional seeded formulae (seeds 200–249, two to five variables): 123 instances, 120 satisfiable and 3 unsatisfiable, 243 target outputs including 240 complete test sets. It uses first and last detecting vectors for each fault, including alternate witness choices.

These finite checks establish observed executable behavior in their bounded domains. The general claim rests on [`proof.md`](proof.md); inputs with more variables and arbitrary valid target witness choices are covered by the proof, not enumeration. Output fault simulation includes output observation after replacement. No throughput or target-solver performance claim was measured.
