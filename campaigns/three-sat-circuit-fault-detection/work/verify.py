"""Separate exhaustive finite check of injected target instances."""

import argparse
import itertools
import json
import random
import subprocess
import sys


def call(path, value, extract=False):
    cmd = [sys.executable, path] + (["--extract"] if extract else [])
    result = subprocess.run(cmd, input=json.dumps(value), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def source_answers(source):
    for bits in itertools.product((0, 1), repeat=source["n"]):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in source["clauses"]):
            yield list(bits)


def circuit_value(target, bits, fault=None):
    wires = list(bits)
    for i in range(len(wires)):
        if fault == (i, 0) or fault == (i, 1):
            wires[i] = fault[1]
    for gate in target["gates"]:
        pins = [wires[i] for i in gate["in"]]
        value = {"not": lambda: 1 - pins[0], "and": lambda: pins[0] & pins[1], "or": lambda: pins[0] | pins[1]}[gate["op"]]()
        wires.append(fault[1] if fault is not None and fault[0] == len(wires) else value)
    return [wires[i] for i in target["outputs"]]


def solve_target(target):
    assert target["inputs"] >= 0 and target["outputs"] and target["designated"]
    for i, gate in enumerate(target["gates"]):
        assert gate["op"] in ("not", "and", "or")
        assert len(gate["in"]) == (1 if gate["op"] == "not" else 2)
        assert all(0 <= p < target["inputs"] + i for p in gate["in"])
    assert all(0 <= p < target["inputs"] + len(target["gates"]) for p in target["outputs"] + target["designated"])
    vectors = list(itertools.product((0, 1), repeat=target["inputs"]))
    tests = {}
    for wire in target["designated"]:
        for stuck in (0, 1):
            tests[wire, stuck] = [list(v) for v in vectors if circuit_value(target, v) != circuit_value(target, v, (wire, stuck))]
            if not tests[wire, stuck]:
                return ["NO-SOLUTION"]
    return [[{"wire": wire, "stuck": stuck, "input": choices[index]} for (wire, stuck), choices in tests.items()]
            for index in (0, -1)]


def cases():
    clauses = list(itertools.product((-1, 1), repeat=3))
    for length in (0, 1, 2):
        for formula in itertools.product(clauses, repeat=length):
            yield {"n": 1, "clauses": [list(c) for c in formula]}
    for seed in range(200, 250):
        rng = random.Random(seed)
        n = 2 + seed % 4
        yield {"n": n, "clauses": [[rng.choice((-1, 1)) * rng.randint(1, n) for _ in range(3)] for _ in range(1 + seed % 9)]}


def main(path):
    instances = outputs = alternatives = positive = negative = 0
    for source in cases():
        sat = list(source_answers(source))
        target = call(path, source)
        for answer in solve_target(target):
            recovered = call(path, {"source": source, "target_solution": answer}, True)
            assert (recovered in sat) if sat else (recovered == "NO-SOLUTION"), (source, answer, recovered)
            outputs += 1
            alternatives += int(answer != "NO-SOLUTION")
        instances += 1
        positive += bool(sat)
        negative += not sat
    print(f"Independent verification passed: {instances} instances ({positive} YES, {negative} NO), {outputs} outputs, {alternatives} complete test sets")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    main(parser.parse_args().candidate)
