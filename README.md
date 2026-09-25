# 3-SAT → Fault detection in logic circuits

Independent research campaign. Status: **ready for expert review** as a reconstruction of the classical output-fault hardness mechanism, not a new complexity theorem. The rule maps a 3-CNF formula to a circuit with sole designated output `w = z AND φ`; every valid complete fault test set yields a satisfying assignment, and target `NO-SOLUTION` yields source `NO-SOLUTION`.

[State](campaigns/three-sat-circuit-fault-detection/state.md) · [Question](campaigns/three-sat-circuit-fault-detection/question.md)

[Algorithm](campaigns/three-sat-circuit-fault-detection/work/algorithm.py) · [Proof](campaigns/three-sat-circuit-fault-detection/work/proof.md) · [Paper PDF](campaigns/three-sat-circuit-fault-detection/work/manuscript.pdf) · [Follow-up independent review](campaigns/three-sat-circuit-fault-detection/reviews/002/review.md) · [Verification](campaigns/three-sat-circuit-fault-detection/work/verification.md)

Reproduce from this repository root:

```sh
uv sync --locked
uv run python campaigns/three-sat-circuit-fault-detection/work/check.py --self-test
uv run python campaigns/three-sat-circuit-fault-detection/work/check.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py
uv run python campaigns/three-sat-circuit-fault-detection/work/verify.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py
uv run python campaigns/three-sat-circuit-fault-detection/reviews/002/check_repaired_cli.py
```

The prepared loop covers 115 source instances and 201 valid target outputs; the separate checker covers 123 instances and 243 outputs. These finite checks support the implementation; the general correctness argument is in the proof and paper. Formalization and expert certification are pending.

Board source commit: 4c2dee3448402208379b169663647146233f04ee.
