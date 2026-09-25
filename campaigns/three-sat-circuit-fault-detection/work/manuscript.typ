#import "report.typ": research-report
#show: research-report.with(
  title: "A search reduction from 3-CNF satisfiability to output-line fault detection",
  date: "25 September 2026",
  status: "Reconstruction for expert review",
)
#set math.equation(numbering: "(1)")

#heading(numbering: none)[Abstract]
Detecting both stuck-at polarities on a circuit output asks whether that output can take both Boolean values. We turn a three-literal CNF formula $phi$ into the single-output circuit $w = z ∧ phi(x)$, where $z$ is a fresh input. The stuck-at-1 fault always has a test, while a stuck-at-0 test exists exactly when $phi$ is satisfiable. Every complete target test set therefore yields a satisfying assignment, and the target's no-solution answer decodes to source no-solution. The construction uses at most $6m$ gates for $m >= 1$ clauses and has polynomial bit complexity even when the variable count is binary encoded. This is an explicit search reconstruction of a classical output-fault hardness mechanism.

= Introduction

A stuck-at fault forces one circuit signal to a fixed bit. A test detects the fault when the faulty and fault-free circuits give different outputs on the same input. Ibarra and Sahni identified output-line detectability with nonconstancy of the circuit function in their Theorem 3.4(1) [1]. Their hardness proof uses a Boolean source framed through 3-DNF tautology. Here the source is the search problem for three-literal CNF, and the target must return tests for both polarities or an explicit no-solution answer. The reduction must recover a source output from every valid target output.

The main result supplies that complete rule. A fresh input $z$ makes the circuit output zero regardless of the formula, while setting $z=1$ exposes its satisfying assignments. The same final wire is both observed and faulted. @fig:construction shows the signal path.

#figure(
  align(center, grid(
    columns: (auto, 14mm, auto, 14mm, auto),
    align: center,
    inset: 5pt,
    [$x_1, dots, x_n$],
    [$arrow.r$],
    [#box(stroke: 0.8pt, inset: 7pt)[$phi(x)$]],
    [$arrow.r$],
    [#box(stroke: 0.8pt, inset: 7pt)[$w = z ∧ phi(x)$]],
  )),
  caption: [The formula circuit feeds the final AND gate together with the independent input $z$. The final wire $w$ is the sole observed output and sole designated fault location; either stuck-at polarity replaces its value at the output.],
) <fig:construction>

= Problems and encoding

A source instance consists of a nonnegative variable count $n$ and a list of $m$ clauses. Each clause has exactly three signed, nonzero indices with absolute value at most $n$. Repeated literals are allowed; an empty clause list denotes the true formula. A valid source output is a length-$n$ bit vector satisfying every clause, or #raw("NO-SOLUTION") precisely when no such vector exists. We write its valid-output set as $S_A(phi)$.

A target instance is an acyclic Boolean circuit represented by its input count and a topologically ordered list of fan-in-two AND/OR gates and fan-in-one NOT gates. Inputs and gate outputs have consecutive wire indices. Lists identify observed outputs and designated fault wires. A single stuck-at-$b$ fault replaces the signal on its designated wire by $b$ before downstream use or output observation. A target output contains one detecting input vector for each designated wire and each polarity $b in {0,1}$. If any required fault has no detecting vector, its only valid output is #raw("NO-SOLUTION"). We write the target valid-output set as $S_B(C)$. The order and choice of detecting vectors are unrestricted.

The input count is a numeric field; an input wire is indexed without a separate gate record. This is the gate-list convention used by the executable contract. A complete target output nevertheless writes every bit of each test vector explicitly. These encoding facts matter when $n$ is much larger than the bit length of its numeric representation.

= Construction and recovery

For each source $phi$, introduce one fresh input $z$. Build a gate for each used negative literal, a two-gate OR tree for each clause, and an AND tree joining the clauses. For $m=0$, use $z ∨ ¬ z$ for the true formula signal. Append one AND gate computing

$ w(x,z) = z ∧ phi(x). $ <eq:output>

Make its output wire the sole observed output and the sole designated fault wire. The algorithm names wires in gate-list order, so all gate inputs refer to earlier wires. It returns a legal target circuit $F(phi)$.

Recovery $G(phi,y)$ returns #raw("NO-SOLUTION") when $y$ is the target no-solution answer. Otherwise, it reconstructs the final wire index from $phi$, locates the stuck-at-0 entry in $y$, and returns the first $n$ bits of that entry's input vector. Reconstructing the index uses only $phi$; it does not rely on state saved by the forward process.

= Correctness

*Lemma 1 (output-fault test).* If a wire $w$ is both a circuit output and the fault location, a stuck-at-$b$ fault is detected by an input precisely when the fault-free value of $w$ equals $1-b$.

_Proof._ Under the fault, the observed value is $b$. Without the fault, the observed value is $w$. The two outputs differ exactly when $w != b$.

*Lemma 2 (the two polarities).* In $F(phi)$, stuck-at-1 is always detectable. Stuck-at-0 is detectable if and only if $phi$ has a satisfying assignment.

_Proof._ Taking $z=0$ makes $w=0$ in @eq:output, so Lemma 1 supplies a stuck-at-1 test. A stuck-at-0 test exists exactly when $w=1$ on some input. @eq:output gives $w=1$ exactly when $z=1$ and $phi(x)=1$. The argument includes an empty clause list.

*Theorem (search reduction).* For every legal three-literal CNF $phi$ and every $y in S_B(F(phi))$, the output $G(phi,y)$ belongs to $S_A(phi)$.

_Proof._ If $phi$ is unsatisfiable, Lemma 2 makes stuck-at-0 undetectable. The target semantics then admit exactly #raw("NO-SOLUTION"), and $G$ returns the valid source no-solution answer. If $phi$ is satisfiable, Lemma 2 makes both polarities detectable, so every valid target output is a complete two-entry test set. Its stuck-at-0 entry detects a fault on the output wire. Lemma 1 and @eq:output imply that the corresponding input has $phi(x)=1$. Recovery returns this $x$, independently of entry order and test-vector choice. Both cases have at least one valid target output, so the implication is not vacuous.

= Bit complexity

Let $L$ be the bit length of the encoded source and $m$ its number of clauses. At most $3m$ distinct negative literals are used. For $m >= 1$, the construction uses at most $3m$ NOT gates, $2m$ clause OR gates, $m-1$ joining AND gates, and one final AND gate: at most $6m$ gates. For $m=0$, it uses three gates. Each wire index takes $O(log(n+m+2))$ bits. Thus the target encoding has $O((m+1) log(n+m+2))$ bits. Since $m <= L$ and $log(n+1) = O(L)$, construction and serialization take polynomial bit time in $L$.

Recovery reconstructs this compact circuit and scans its target output $y$. For a complete output, $y$ contains explicit input vectors of length $n+1$, so copying the recovered $n$ bits is bounded by $|y|$. For #raw("NO-SOLUTION"), recovery writes a fixed string. Its running time and output length are polynomial in $L+|y|$. Both maps are deterministic and call no solver. The target solver's work is outside these bounds.

= Relation to earlier work

Ibarra and Sahni's output-line result [1] states the nonconstancy criterion for detecting both output faults. The construction above uses that criterion with a fresh gating input to connect the fixed 3-CNF search source to complete target test sets. It gives an explicit decoder and treats the no-solution case. It does not establish a new hardness theorem or a first use of the gating step. The original paper also studies finding test sets under an irredundancy promise in Theorem 3.5; our target instead has an explicit no-solution output when a required fault is undetectable.

= Conclusion

The gated formula output gives a total polynomial-time instance map and recovery map for the stated fault model. Its proof handles both stuck-at polarities, satisfiable and unsatisfiable formulas, and every valid target output. The target solver can still require exponential work, and the reduction makes no practical speed claim.

#heading(numbering: none)[References]

[1] O. H. Ibarra and S. K. Sahni, “Polynomially Complete Fault Detection Problems,” _IEEE Transactions on Computers_ C-24(3), 242–249 (1975). Section II, problem P4; Theorem 3.4(1) and Theorem 3.5, Case 4. #link("https://www.cise.ufl.edu/~sahni/papers/faultDetection.pdf")[Primary-source PDF].

#set heading(numbering: "A.")
#counter(heading).update(0)
= Verification and reproducibility

The executable source and target encodings are specified in #raw("contract.md"); the two maps are in #raw("algorithm.py"). Python 3.12.14, uv 0.12.17 and Z3 5.1.0 were used for the prepared corpus. Typst 0.15.1 compiled this manuscript. Run from the repository root:

#raw("uv sync --locked", block: true, lang: "sh")
#raw("uv run python campaigns/three-sat-circuit-fault-detection/work/check.py --self-test", block: true, lang: "sh")
#raw("uv run python campaigns/three-sat-circuit-fault-detection/work/check.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py", block: true, lang: "sh")
#raw("uv run python campaigns/three-sat-circuit-fault-detection/work/verify.py --candidate campaigns/three-sat-circuit-fault-detection/work/algorithm.py", block: true, lang: "sh")
#raw("uv run python campaigns/three-sat-circuit-fault-detection/reviews/001/check_large_input.py", block: true, lang: "sh")
#raw("uv run python campaigns/three-sat-circuit-fault-detection/reviews/002/check_repaired_cli.py", block: true, lang: "sh")

The prepared corpus has 115 source formulas: 100 seeded random formulas of three to six variables and 15 hand-designed edge cases of zero to four variables. Z3 independently labels satisfiability; exhaustive fault simulation solves each generated target with at most seven inputs. The candidate loop checked 201 valid target outputs. A second checker, using separate exhaustive source and target solvers, checked 123 more source formulas with one to five variables and 243 target outputs, including alternate complete test sets. The last two commands exercise a 4,301-digit input count at the CLI boundary. These are finite checks; the theorem above supplies the unrestricted correctness argument.

The default #raw("algorithm.py") mode reads one source JSON object from standard input and writes the target JSON. Its #raw("--extract") mode reads a JSON object with keys #raw("source") and #raw("target_solution") and writes the recovered source output. The two modes may run in separate fresh processes. No command uses a timeout.
