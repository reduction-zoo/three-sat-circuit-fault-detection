"""Check forward-map totality for a legal, compact large-input source."""

import json
import subprocess
import sys
from pathlib import Path


candidate = Path(__file__).resolve().parents[2] / "work" / "algorithm.py"
sys.set_int_max_str_digits(0)
n_text = "1" + "0" * 4300
source = '{"n":' + n_text + ',"clauses":[]}'
result = subprocess.run([sys.executable, str(candidate)], input=source, text=True, capture_output=True)
assert result.returncode == 0, result.stderr
target = json.loads(result.stdout)
assert target["inputs"] == int(n_text) + 1
assert target["outputs"] == target["designated"]
assert len(target["outputs"]) == 1
print("Large-input construction passed")
