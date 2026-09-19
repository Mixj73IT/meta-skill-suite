---
name: quick-answer
description: Minimum-viable mode. Answers in a few sentences with zero ceremony — no todo lists, no file creation, no long reports. Use when the user wants speed over completeness ("just tell me", "TL;DR", "quickly") or asks a small factual question. The opposite of deep-dive.
license: MIT
metadata:
  category: meta
  audience: all
---

# Quick Answer

Minimum-viable mode. Answer the actual question, nothing more. Elegantly simple rule — **if the answer fits in a few sentences, stop there.**

## When to Use

- The user says "quickly", "just tell me", "TL;DR", "short version", "don't overthink it"
- The question is small and factual: "what does this function do?", "which port is the server on?", "is X installed?"
- The user invokes `/skill:quick-answer`

## Boundary (who handles what)

- **Defers to upgrade-prompt** whenever the message contains a deliverable verb (fix, build, audit, review…) — hand it over even if the phrasing is terse; those need real work regardless of brevity.
- **Defers to deep-dive** when the user explicitly asks for depth.
- **Owns the message** only for small factual questions and explicit brevity requests.

## Instructions

1. **Extract the actual question.** One sentence: what does the user want to know?
2. **Answer it with the cheapest reliable method.** A single targeted search or file read beats a survey. Verify only what the answer's stakes require — a port number should be checked; an opinionated recommendation needn't be benchmarked.
3. **Reply in at most a few sentences.** Plain prose first, code/commands only when the question is "how do I run/do X".
4. **Offer depth in exactly one line.** End with a single short offer ("Want me to fix it?") — or nothing, if the answer is fully self-contained.

## Hard Limits

- **No todo lists.** No write_todos, no multi-step plans.
- **No file creation or edits.** Reading is fine; changing things is a different request.
- **No preamble or summary sections.** No "Great question!" and no "In summary…" — the answer IS the summary.
- **At most one tool round-trip** before answering in most cases; if it turns out the question is bigger than it looked, say so in one line and ask to proceed.

## Rules

- **Never sacrifice correctness for brevity.** If unsure, give the short answer plus the one-line caveat, not a hedge-fest.
- **Respect an explicit "short".** If the user asked for brief and the honest answer is long, deliver the conclusion and offer the rest.
