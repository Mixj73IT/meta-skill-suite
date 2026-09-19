---
name: deep-dive
description: Maximum-depth mode. Performs exhaustive investigation and long-form reporting with verification at every step. Use when the user asks for a deep dive, thorough analysis, "go deep", "don't hold back", or when a topic genuinely warrants full rigor. The opposite of quick-answer.
license: MIT
metadata:
  category: meta
  audience: all
---

# Deep Dive

Maximum-depth mode. Where default behavior balances speed and thoroughness, this skill removes the speed term: investigate exhaustively, verify everything, and report at full length. Elegantly simple rule — **one pass is never enough.**

## When to Use

- The user says "deep dive", "go deep", "thorough", "exhaustive", "don't hold back", "leave no stone unturned"
- The user invokes `/skill:deep-dive`
- The stakes are high (production incident, security review, architectural decision) and being wrong is expensive

## Boundary (who handles what)

- **Defers to quick-answer** when the question is small and factual — depth there is noise, not rigor.
- **Defers scope to upgrade-prompt** when the message is a bare imperative without a depth request ("Audit this"): take that skill's expanded scope, run it at this skill's rigor.
- **Owns the message** when the user explicitly asks for depth or the stakes demand it.

## Instructions

1. **Frame the question.** Restate what is being investigated and what a complete answer must contain. Define the boundary of the investigation up front.
2. **Gather from multiple angles.** Read all relevant code/docs end to end — not just search hits. Search the web for prior art and known pitfalls. Check git history for why things are the way they are (if the workspace isn't a git repo, note that and skip this angle). Where an area has more than one plausible interpretation, investigate all of them.
3. **Verify every claim.** Run the code, the tests, the typechecker, the benchmark. No assertion in the final report may rest on a reading alone. Mark anything unverifiable explicitly as such.
4. **Stress-test your own conclusion.** Before writing up, argue the opposite position: what evidence would contradict your findings? If you can't name any, look harder. Where uncertainty remains, quantify it (what you'd need to check to resolve it).
5. **Report in full.** Use the report structure below. Length is earned by evidence — every section must say something, no filler.

## Report Structure

1. **Executive Summary** — the answer, in ~5 bullets, for the reader who stops here.
2. **Method** — what was examined, what was run, what sources were consulted (so findings can be reproduced or challenged).
3. **Findings** — the core analysis, ordered by importance. Each claim backed by evidence (file:line, command output, citation).
4. **Counter-evidence and open questions** — what cuts against the conclusion, what couldn't be verified, what deserves follow-up.
5. **Recommendations** — concrete next actions, ordered, each small enough to act on directly.
6. **Appendix** — raw evidence worth keeping: command outputs, traces, relevant excerpts.

## Rules

- **No hand-waving.** "It probably works" is a finding only if followed by the test that would settle it.
- **Show the method.** Every conclusion is traceable to something the reader could re-run.
- **Depth ≠ length.** Cut anything that doesn't change the reader's understanding; never pad.
- **Play well with siblings.** Pairs naturally with upgrade-prompt: "deep-dive audit of this" = upgraded scope + full rigor.
