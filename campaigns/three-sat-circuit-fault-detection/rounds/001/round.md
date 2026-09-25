# Round 001 — gated formula output

## Plan (recorded before construction)

Gap: both stuck-at polarities must be required, while a valid complete target output must expose a source assignment. Mechanism: compute `w = z AND φ(x)` and designate/output only `w`. The fresh `z` should make stuck-at-1 always detectable; stuck-at-0 should be detectable exactly when `φ` is satisfiable. Recovery should take the `x` bits from any stuck-at-0 witness, or map target `NO-SOLUTION` to source `NO-SOLUTION`.

Prior evidence: Prepare commit `8144bb9` fixes 115 source cases and independent target simulation. The board shared experience directory has no available entries. First discriminating check: run the fixed `check.py --candidate` loop against a complete executable rule. A failure will be diagnosed as construction, oracle or recovery behavior before changing strategy.

## Evidence and diagnosis

The executable rule is [`algorithm.py`](../../work/algorithm.py) and the general argument is [`proof.md`](../../work/proof.md). The prepared loop passed 115 actual target instances and 201 valid outputs, including 28 `NO-SOLUTION` cases. Independent [`verify.py`](../../work/verify.py) passed 123 further instances and 243 outputs, including alternate complete test sets. Exact commands and domains: [`verification.md`](../../work/verification.md). No counterexample or oracle defect was observed. The proof reduces output fault detectability to the value of `w = z AND φ`; both polarities and all valid target outputs are handled. Acyclicity, gate count and encoding bounds are explicit.

Primary literature check on 2026-09-25: Ibarra–Sahni (1975), Theorem 3.4(1), treats output-fault detectability via nonconstancy, from a 3-DNF tautology formulation. The present `z` gate and recovery reconstruct the fixed 3-CNF search question. The upstream issue describes the simpler stuck-at-0 idea but does not handle required stuck-at-1 universally. This is a known hardness mechanism, not a new complexity theorem.

Independent [review 001](../../reviews/001/review.md) found a legal 4,301-digit input count that caused Python's default integer conversion cap to reject the CLI input. It also found that a count-based `O(n+m)` estimate alone does not prove polynomial time when `n` is binary encoded. The reviewer retained a targeted failing check. The CLI now accepts unbounded finite decimal counts and the proof bounds gates by `6m` and bit complexity by input/output encoding lengths. The targeted check passes; the prepared and separate verification loops were rerun without changed counts. This is a same-strategy repair, so it remains round 001. Fresh-context [review 002](../../reviews/002/review.md) advanced the repaired result. The [Typst paper](../../work/manuscript.pdf) compiled to three pages and was visually inspected on 2026-09-25.

Experience extraction: none; the polarity gate is part of this complete rule, and the classical output-fault characterization is cited in the proof. There is no failed search lesson to generalize.

## Next action

Round closed. Seek expert review; formalization was not requested. No second construction round is needed. Remaining budget: 19 rounds.
