# Fixed question

```json
{
  "source": "3-SAT",
  "target": "Fault detection in logic circuits",
  "category": "Construction open",
  "summary": "An explicit rule connects satisfiability to automatic generation of inputs that expose hardware faults.",
  "source_definition": "Given a three-literal Boolean CNF formula, return a satisfying assignment, or NO-SOLUTION exactly when it is unsatisfiable. All finite combinatorial structures are explicit and numerical data use binary encoding.",
  "target_definition": "Given an explicitly represented acyclic Boolean circuit, output wires and a designated set of signal wires, return, for each designated wire and each stuck-at value 0 or 1, an input assignment for which that single fault changes an output. Return NO-SOLUTION if any required fault is undetectable.",
  "required_result": "Construct deterministic polynomial-time maps F and G. F must produce a legal target instance, and G(x,y) must return a valid source output for every valid target output y, including NO-SOLUTION. A complete rule may reconstruct a published construction or give a new one; it must specify every gadget, numerical parameter and decoding step.",
  "acceptance": "Deliver executable instance construction and output recovery, a general proof covering all legal inputs and target outputs, and worst-case polynomial time and encoding-size bounds. Cite the actual proof used, or identify a newly derived argument. Check small positive and negative instances with independent solvers; finite tests alone do not establish correctness.",
  "importance": "An explicit rule connects satisfiability to automatic generation of inputs that expose hardware faults.",
  "difficulty": "Difficulty is not yet established by a construction attempt. Fault detection requires distinguishing a faulty circuit from the fault-free one. The construction must account for both stuck-at polarities and recover a satisfying assignment from any complete test set.",
  "openness": "The cited source requests a reconstruction of a classical fault-testing hardness rule. The cited paper uses a different Boolean source formulation; a complete answer must supply and justify the connecting transformation.",
  "literature_checked": "2026-09-18",
  "coverage": "Import inventory review of the cited sources. Primary proofs have not been independently re-audited; availability of a complete reconstruction elsewhere remains unassessed.",
  "references": [
    {
      "title": "Problem-Reductions: 3-SAT \u2192 Fault detection in logic circuits",
      "url": "https://github.com/CodingThrust/problem-reductions/issues/919",
      "note": "Upstream issue and review discussion checked on 2026-09-18. Its references are reconstruction leads, not independently audited proof sources."
    }
  ],
  "solutions": [],
  "equation": ""
}
```
