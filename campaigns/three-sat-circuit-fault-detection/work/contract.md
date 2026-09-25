# Executable problem contract

Source input: `{"n": N, "clauses": [[a,b,c], ...]}`. `N` is a nonnegative integer; every literal is a nonzero signed integer of absolute value at most `N`. Repeated literals and empty clause lists are legal. Source output is a length-`N` list of Boolean bits satisfying every clause, or the string `"NO-SOLUTION"` exactly when none exists.

Target input: `{"inputs": K, "gates": [{"op": "and|or|not", "in": [wire,...]}, ...], "outputs": [wire,...], "designated": [wire,...]}`. Wires `0,...,K-1` are inputs; gate `j` defines wire `K+j` and refers only to earlier wires. `not` has one input, `and` and `or` have two. Outputs and designated wires are nonempty lists of distinct valid wires. A fault on wire `w` forces its signal to bit `b` after its driver and before fanout or output observation. The fault is detectable by a length-`K` bit vector iff at least one listed output differs from the fault-free circuit. An output wire may be designated.

Target output is `"NO-SOLUTION"` exactly when any designated wire/polarity pair is undetectable. Otherwise it is a list of objects `{"wire": w, "stuck": b, "input": [bits...]}`, with exactly one object for each designated wire and each bit `b ∈ {0,1}`; each input must detect its listed fault. Entry order and witness choices are arbitrary.

`algorithm.py` reads one source JSON object on standard input and writes one target JSON object on standard output. With `--extract`, it reads `{"source": source, "target_solution": output}` and writes a valid source output. Both modes run in separate processes; diagnostics go to standard error, and errors exit nonzero. The checker validates target outputs from the definition above rather than from the candidate.
