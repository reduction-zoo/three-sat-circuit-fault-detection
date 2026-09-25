# Prepare evidence

Fixed on 2026-09-25 before any candidate: [`cases.json`](cases.json) has 115 distinct legal 3-CNF sources, including 100 seeded random cases (seeds 0–99) and 15 hand-designed edge cases. Random sizes are 25 each for 3, 4, 5, and 6 variables; edge sizes are 0:1, 1:5, 2:4, 3:4, 4:1. The corpus contains 87 satisfiable and 28 unsatisfiable formulas according to Z3 5.1.0. Random sources regenerate with `generate_cases.py` and each recorded seed. Regeneration intentionally does not relabel expected decisions; `check.py --self-test` recomputes them independently.

`check.py` encodes each source clause as a Z3 disjunction. A satisfying Z3 model gives a direct 3-CNF assignment; conversely each satisfying assignment satisfies those same disjunctions. Only `sat` and `unsat` count as conclusive. Every returned assignment is checked directly against the clauses. A small hand oracle covers empty formula, a unit clause, and contradictory units.

The target oracle exhaustively enumerates every input bit vector and simulates the fault-free circuit and each single stuck-at fault. A vector is retained only when an output differs. Exhaustion proves undetectability within the explicitly represented finite input domain; it does not rely on candidate code or a target solver. Target output validation checks every required wire/polarity pair, distinctness and direct detection. Self-tests include an undetectable wire, propagated input fault, false detection witness, false `NO-SOLUTION`, invalid source witness and a false satisfiability claim. The target oracle is practical only for small circuits; campaign tests use at most seven inputs.

Run from repository root:

```sh
uv sync --locked
uv run python campaigns/three-sat-circuit-fault-detection/work/check.py --self-test
```

Observed: corpus gate passed (115 distinct, 100 random, 15 edge); self-test passed (87 YES, 28 NO). The future `--candidate PATH` mode will run each instance map in a subprocess, solve its actual target, pass canonical and alternate complete target outputs to a fresh extraction subprocess, and validate recovered source outputs. Alternate outputs are generated when at least one fault has multiple detecting vectors.
