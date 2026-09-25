"""3-SAT to complete stuck-at fault detection; JSON on stdin/stdout."""

import json
import sys


def construct(source):
    n = source["n"]
    z = n
    gates = []

    def gate(op, *pins):
        wire = n + 1 + len(gates)
        gates.append({"op": op, "in": list(pins)})
        return wire

    negatives = {}

    def literal(a):
        if a > 0:
            return a - 1
        i = -a - 1
        if i not in negatives:
            negatives[i] = gate("not", i)
        return negatives[i]

    clauses = []
    for a, b, c in source["clauses"]:
        clauses.append(gate("or", gate("or", literal(a), literal(b)), literal(c)))
    if clauses:
        formula = clauses[0]
        for clause in clauses[1:]:
            formula = gate("and", formula, clause)
    else:
        formula = gate("or", z, gate("not", z))
    output = gate("and", z, formula)
    return {"inputs": n + 1, "gates": gates, "outputs": [output], "designated": [output]}


def extract(source, target_solution):
    if target_solution == "NO-SOLUTION":
        return "NO-SOLUTION"
    output = construct(source)["outputs"][0]
    for entry in target_solution:
        if entry["wire"] == output and entry["stuck"] == 0:
            return entry["input"][:source["n"]]
    raise ValueError("missing stuck-at-0 witness")


if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
        answer = extract(data["source"], data["target_solution"]) if sys.argv[1:] == ["--extract"] else construct(data)
        json.dump(answer, sys.stdout)
        sys.stdout.write("\n")
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
