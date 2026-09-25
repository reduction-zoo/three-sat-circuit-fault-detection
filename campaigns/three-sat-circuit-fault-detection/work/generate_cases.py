"""Fixed pre-construction 3-CNF corpus."""

import json
import random
from pathlib import Path


def source_for_seed(seed):
    rng = random.Random(seed)
    n = 3 + seed % 4
    clauses = []
    if seed % 4 == 0:
        clauses.extend([[1, 1, 1], [-1, -1, -1]])
    for _ in range(2 + seed % 8):
        clauses.append([rng.choice((-1, 1)) * rng.randint(1, n) for _ in range(3)])
    return {"n": n, "clauses": clauses}


EDGES = [
    {"n": 0, "clauses": []},
    {"n": 1, "clauses": []},
    {"n": 1, "clauses": [[1, 1, 1]]},
    {"n": 1, "clauses": [[-1, -1, -1]]},
    {"n": 1, "clauses": [[1, 1, 1], [-1, -1, -1]]},
    {"n": 1, "clauses": [[1, -1, 1]]},
    {"n": 2, "clauses": [[1, 1, 1], [2, 2, 2]]},
    {"n": 2, "clauses": [[1, 1, 1], [-2, -2, -2]]},
    {"n": 2, "clauses": [[1, 2, 2], [-1, -2, -2]]},
    {"n": 2, "clauses": [[1, 1, 1], [-1, 2, 2], [-2, -2, -2]]},
    {"n": 3, "clauses": [[1, 2, 3]]},
    {"n": 3, "clauses": [[-1, -2, -3]]},
    {"n": 3, "clauses": [[1, 1, 1], [2, 2, 2], [3, 3, 3]]},
    {"n": 3, "clauses": [[1, 1, 1], [-1, -1, -1], [2, 3, 3]]},
    {"n": 4, "clauses": [[1, -1, 2], [3, -3, 4]]},
]


if __name__ == "__main__":
    cases = ([{"source": x, "kind": "edge"} for x in EDGES] +
             [{"source": source_for_seed(s), "kind": "random", "seed": s} for s in range(100)])
    Path(__file__).with_name("cases.json").write_text(json.dumps(cases, indent=2) + "\n")
