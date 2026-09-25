"""Exercise both CLI maps past Python's former integer conversion limit."""

import json
import subprocess
import sys
from pathlib import Path


candidate = Path(__file__).resolve().parents[2] / "work" / "algorithm.py"
large_count = "1" + "0" * 4300
source = '{"n":' + large_count + ',"clauses":[[1,1,1],[-1,-1,-1]]}'

constructed = subprocess.run(
    [sys.executable, str(candidate)], input=source, text=True, capture_output=True
)
assert constructed.returncode == 0, constructed.stderr
target = json.loads(constructed.stdout, parse_int=str)
assert target["inputs"] == large_count[:-1] + "1"
assert len(target["gates"]) == 7
assert target["outputs"] == target["designated"] == [large_count[:-1] + "7"]

extracted = subprocess.run(
    [sys.executable, str(candidate), "--extract"],
    input='{"source":' + source + ',"target_solution":"NO-SOLUTION"}',
    text=True,
    capture_output=True,
)
assert extracted.returncode == 0, extracted.stderr
assert json.loads(extracted.stdout) == "NO-SOLUTION"
print("Large-count construction and recovery passed")
