# 3-SAT → Fault detection in logic circuits

**Status:** ready for expert review · **Research model:** gpt-6-sol · **Submitted:** 2026-09-25

This repository reconstructs a classical fault-detection hardness mechanism for the fixed search contract. Deterministic polynomial-time maps construct a legal circuit from a three-literal CNF formula and recover a satisfying assignment from **every** valid complete fault-test output. Target `NO-SOLUTION` recovers source `NO-SOLUTION`. This is a reconstruction, not a new complexity theorem.

## Construction

For formula φ(x), introduce a fresh input z and make `w = z AND φ(x)` the sole observed output and designated fault wire. Stuck-at-1 is always detectable with z = 0. Stuck-at-0 is detectable exactly when φ is satisfiable; any detecting input contains a satisfying assignment in its x bits.

## Evidence

- **Correctness and recovery:** The general proof covers legal inputs, both polarities, all valid target outputs, and `NO-SOLUTION`. The registered independent reviewer advanced the repaired rule; human expert acceptance remains pending. [Proof](campaigns/three-sat-circuit-fault-detection/work/proof.md) · [review](campaigns/three-sat-circuit-fault-detection/reviews/002/review.md)
- **Bit complexity:** At most 6m gates for m ≥ 1 clauses, or three gates for the empty formula. The bound accounts for binary-encoded variable counts and explicit target witness length. [Proof](campaigns/three-sat-circuit-fault-detection/work/proof.md)
- **Executable verification:** The prepared loop checked 115 source instances and 201 valid target outputs. A separate exhaustive checker checked 123 instances and 243 outputs. Targeted CLI checks cover a 4,301-digit variable count. Finite checks do not replace the proof. [Evidence](campaigns/three-sat-circuit-fault-detection/work/verification.md)
- **Formal and human checks:** No Lean proof, human expert acceptance, or upstream integration is recorded. [State](campaigns/three-sat-circuit-fault-detection/state.md)

## Reproduce

Run from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/three-sat-circuit-fault-detection/work/check.py --self-test
uv run --locked python campaigns/three-sat-circuit-fault-detection/work/check.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py
uv run --locked python campaigns/three-sat-circuit-fault-detection/work/verify.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py
uv run --locked python campaigns/three-sat-circuit-fault-detection/reviews/002/check_repaired_cli.py
```

These commands check bounded source and target instances through construction, independent target solving and output recovery. The unrestricted claim rests on the written proof.

## Artifacts

- [Fixed question](campaigns/three-sat-circuit-fault-detection/question.md)
- [Campaign state](campaigns/three-sat-circuit-fault-detection/state.md)
- [Manuscript](campaigns/three-sat-circuit-fault-detection/work/manuscript.pdf)
- [Construction and recovery](campaigns/three-sat-circuit-fault-detection/work/algorithm.py)
- [General proof](campaigns/three-sat-circuit-fault-detection/work/proof.md)
- [Independent review](campaigns/three-sat-circuit-fault-detection/reviews/002/review.md)
- [Verification evidence](campaigns/three-sat-circuit-fault-detection/work/verification.md)

Board source commit: 4c2dee3448402208379b169663647146233f04ee.
