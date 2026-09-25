"""Independent source and target oracles and the fixed-corpus candidate gate."""

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path

import z3

from generate_cases import source_for_seed

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NO = "NO-SOLUTION"


def bits(value, length):
    return isinstance(value, list) and len(value) == length and all(type(x) is int and x in (0, 1) for x in value)


def source_legal(src):
    if not isinstance(src, dict) or type(src.get("n")) is not int or src["n"] < 0 or not isinstance(src.get("clauses"), list):
        return False
    n = src["n"]
    return all(isinstance(c, list) and len(c) == 3 and all(type(a) is int and 0 < abs(a) <= n for a in c) for c in src["clauses"])


def source_valid(src, answer, satisfiable):
    if answer == NO:
        return not satisfiable
    if not bits(answer, src["n"]):
        return False
    return all(any(answer[abs(a) - 1] == int(a > 0) for a in c) for c in src["clauses"])


def solve_source(src):
    assert source_legal(src)
    variables = [z3.Bool(f"x{i}") for i in range(src["n"])]
    solver = z3.Solver()
    for clause in src["clauses"]:
        solver.add(z3.Or(*[variables[abs(a) - 1] if a > 0 else z3.Not(variables[-a - 1]) for a in clause]))
    result = solver.check()
    if result == z3.unsat:
        return NO
    if result != z3.sat:
        raise RuntimeError(f"inconclusive source oracle: {result}")
    answer = [int(z3.is_true(solver.model().eval(x, model_completion=True))) for x in variables]
    assert source_valid(src, answer, True)
    return answer


def target_legal(target):
    if not isinstance(target, dict) or type(target.get("inputs")) is not int or target["inputs"] < 0 or not isinstance(target.get("gates"), list):
        return False
    k = target["inputs"]
    for gate in target["gates"]:
        if not isinstance(gate, dict) or gate.get("op") not in ("and", "or", "not") or not isinstance(gate.get("in"), list):
            return False
        pins = gate["in"]
        if len(pins) != (1 if gate["op"] == "not" else 2) or any(type(w) is not int or w < 0 or w >= k for w in pins):
            return False
        k += 1
    for name in ("outputs", "designated"):
        seq = target.get(name)
        if not isinstance(seq, list) or not seq or len(set(map(str, seq))) != len(seq) or any(type(w) is not int or w < 0 or w >= k for w in seq):
            return False
    return True


def evaluate(target, assignment, fault=None):
    values = list(assignment)
    if fault is not None and fault[0] < target["inputs"]:
        values[fault[0]] = fault[1]
    for gate in target["gates"]:
        pins = [values[w] for w in gate["in"]]
        value = (1 - pins[0] if gate["op"] == "not" else int(all(pins)) if gate["op"] == "and" else int(any(pins)))
        values.append(fault[1] if fault is not None and fault[0] == len(values) else value)
    return tuple(values[w] for w in target["outputs"])


def detects(target, wire, stuck, assignment):
    return evaluate(target, assignment) != evaluate(target, assignment, (wire, stuck))


def target_witnesses(target):
    assert target_legal(target)
    inputs = list(itertools.product((0, 1), repeat=target["inputs"]))
    possibilities = {}
    for w in target["designated"]:
        for b in (0, 1):
            found = [list(a) for a in inputs if detects(target, w, b, a)]
            if not found:
                return [NO]
            possibilities[w, b] = found
    keys = list(possibilities)
    return [[{"wire": w, "stuck": b, "input": possibilities[w, b][choice % len(possibilities[w, b])]} for w, b in keys]
            for choice in range(min(2, max(map(len, possibilities.values()))))]


def target_valid(target, answer, feasible):
    if answer == NO:
        return not feasible
    expected = {(w, b) for w in target["designated"] for b in (0, 1)}
    if not isinstance(answer, list) or len(answer) != len(expected):
        return False
    seen = set()
    for entry in answer:
        if not isinstance(entry, dict) or set(entry) != {"wire", "stuck", "input"}:
            return False
        w, b, a = entry["wire"], entry["stuck"], entry["input"]
        if type(w) is not int or type(b) is not int or (w, b) not in expected or (w, b) in seen or not bits(a, target["inputs"]) or not detects(target, w, b, a):
            return False
        seen.add((w, b))
    return seen == expected


def run_candidate(path, data, extract=False):
    command = [sys.executable, str(path)] + (["--extract"] if extract else [])
    proc = subprocess.run(command, input=json.dumps(data), text=True, capture_output=True)
    if proc.returncode:
        raise RuntimeError(f"{command}: {proc.stderr}")
    return json.loads(proc.stdout)


def self_test(cases):
    subprocess.run([sys.executable, str(ROOT / "research/validate_preparation.py"), str(HERE / "cases.json")], check=True)
    hand = [({"n": 0, "clauses": []}, True), ({"n": 1, "clauses": [[1, 1, 1]]}, True),
            ({"n": 1, "clauses": [[1, 1, 1], [-1, -1, -1]]}, False)]
    for src, sat in hand:
        got = solve_source(src)
        assert (got != NO) == sat and source_valid(src, got, sat)
    trivial = {"inputs": 1, "gates": [], "outputs": [0], "designated": [0]}
    solutions = target_witnesses(trivial)
    assert all(target_valid(trivial, y, True) for y in solutions)
    assert not target_valid(trivial, NO, True)
    assert not target_valid(trivial, [{"wire": 0, "stuck": 0, "input": [0]}, {"wire": 0, "stuck": 1, "input": [0]}], True)
    hidden = {"inputs": 2, "gates": [], "outputs": [0], "designated": [1]}
    assert target_witnesses(hidden) == [NO] and target_valid(hidden, NO, False)
    propagated = {"inputs": 2, "gates": [{"op": "and", "in": [0, 1]}], "outputs": [2], "designated": [0]}
    assert detects(propagated, 0, 0, [1, 1]) and not detects(propagated, 0, 0, [1, 0])
    assert not source_valid(hand[1][0], [0], True)
    assert not source_valid(hand[2][0], [1], False)
    counts = {"yes": 0, "no": 0}
    for case in cases:
        src = case["source"]
        assert source_legal(src)
        if case["kind"] == "random":
            assert source_for_seed(case["seed"]) == src
        got = solve_source(src)
        assert source_valid(src, got, got != NO)
        assert case["expected"] == ("YES" if got != NO else "NO-SOLUTION")
        counts["yes" if got != NO else "no"] += 1
    print(f"Self-test passed: {len(cases)} cases; {counts}")


def candidate_test(cases, path):
    outputs = 0
    counts = {"yes": 0, "no": 0}
    for i, case in enumerate(cases):
        src = case["source"]
        target = run_candidate(path, src)
        if not target_legal(target):
            raise AssertionError(f"case {i}: illegal target {target}")
        ys = target_witnesses(target)
        for y in ys:
            assert target_valid(target, y, y != NO)
            recovered = run_candidate(path, {"source": src, "target_solution": y}, True)
            if not source_valid(src, recovered, case["expected"] == "YES"):
                raise AssertionError(f"case {i}: source={src}, target={target}, output={y}, recovered={recovered}")
            outputs += 1
        counts["yes" if ys[0] != NO else "no"] += 1
    print(f"Candidate passed: {len(cases)} instances, {outputs} target outputs, {counts}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    cases = json.loads((HERE / "cases.json").read_text())
    self_test(cases) if args.self_test else candidate_test(cases, args.candidate.resolve())
