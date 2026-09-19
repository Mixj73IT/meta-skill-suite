---
name: upgrade-prompt
description: Expands terse user prompts ("Audit this", "Fix this", "Review this") into comprehensive, structured instructions before executing them, adding scope, depth, and a defined output format. Use when the user's message is a bare imperative or very short shorthand, or when they explicitly ask to improve, upgrade, or expand a prompt.
license: MIT
metadata:
  category: meta
  audience: all
---

# Upgrade Prompt

Turn one-line shorthand into a full, professional instruction — then execute it. The user says "Audit this" and means a comprehensive audit with an executive summary and prioritized todos, not a two-paragraph once-over.

## When to Use

Activate this skill when the user's message is:

- A **bare imperative** with no detail: "Audit this", "Review this", "Fix this", "Refactor this", "Add tests", "Document this", "Optimize this", "Make it fast", "Secure this", "Clean this up", "Analyze this", "Plan this", "Ship it", "Deploy this"
- **Very short** (under ~8 words) and refers to a target ("this", "the auth module") without stating depth or format
- An explicit request to **improve, upgrade, enhance, or expand a prompt**
- The user invokes `/skill:upgrade-prompt`

Do NOT activate when the user already gave specifics (target files, constraints, desired format) — just do the work.

## Boundary (who handles what)

- **Defers to quick-answer** when the message is a small factual question with no deliverable verb ("what port is this on?") — terseness alone doesn't mean upgrade.
- **Layers with deep-dive** when the user explicitly asks for depth ("deep-dive audit of this"): keep this skill's expanded scope, apply deep-dive's verification and report structure.
- **Deliverable verbs beat depth words**: "quickly fix this" still routes here — the verb (fix) wins over the adverb (quickly); delivery just stays brisk.

## Instructions

1. **Classify the intent.** Match the terse prompt to an expansion template below (audit, review, fix, build, implement, analyze, test, document, plan, deploy, migrate, optimize, secure). If none fits, treat it as "analyze" with the user's verb as the goal.
2. **Resolve the target.** Figure out what "this" refers to — the current file, a directory, the repo, the last thing discussed. Inspect the code to confirm the target exists and note its scope. If after a quick look there are genuinely multiple plausible targets, ask ONE clarifying question; otherwise proceed with the most reasonable interpretation and state your assumption up front.
3. **Silently expand the prompt** into a structured spec using the matching template: objective, scope, steps, output format, and success criteria. Never lose the user's original intent — you are adding structure and standard professional depth, not redirecting the task.
4. **Announce the expansion in one short line**, e.g. "Running a comprehensive audit of `src/auth/` → findings + executive summary + prioritized todos." Track the expanded steps with a todo list so the user can see what "upgrading" did and follow progress.
5. **Execute the expanded version**, not the literal shorthand.

## Expansion Templates

### Audit
Perform a comprehensive audit of the target. Read the relevant code first; do not audit from assumptions.

- **Scope**: correctness, security (injection, auth, secrets, input validation), error handling, performance, edge cases, test coverage, maintainability, dependency risks, documentation gaps.
- **Output format, in this order**:
  1. **Executive Summary** — 3–5 bullets: overall health, the top risks, and quick wins. Written for someone who reads nothing else.
  2. **Findings** — grouped by severity (Critical / High / Medium / Low), each with file:line references, why it matters, and a concrete recommendation.
  3. **Prioritized Todos** — a checkbox list ordered by impact-to-effort, small enough that each item is a single actionable task.
- Flag what is already done well, not just problems.

### Review
A thorough code review of the target: correctness first, then tests, security, performance, readability, and naming. Give constructive, specific feedback with file:line references; suggest alternatives rather than only criticizing; acknowledge good patterns. End with a verdict (approve / approve with comments / changes requested) and the 3 highest-priority comments.

### Fix
Diagnose before changing: reproduce or trace the bug, state the root cause, then apply the minimal fix that addresses the cause rather than the symptom. Verify with a test that fails before the fix and passes after. Check for the same class of bug nearby.

### Build / Implement
Clarify the goal and constraints, inspect existing patterns in the codebase, plan the approach, implement it following project conventions, then verify: types/lint pass, relevant tests exist and pass, and the feature is demonstrably working. Summarize what was built and how it was tested.

### Analyze
Produce a structured analysis: what the target does, how it works (data flow / architecture), notable strengths, risks, and open questions. Reference specific files and lines. Keep it factual — recommendations only where the evidence supports them.

### Test
Inventory what is untested in the target, prioritize by risk, write tests that follow the project's existing test conventions, and run them. Report coverage gaps that remain.

### Document
Audit what documentation exists and what's missing, then write docs that match the project's existing style: what it is, how to use it, how it works, gotchas. Prefer editing existing docs over creating new ones.

### Plan
Break the goal into ordered, concrete steps with scope, dependencies, risks, and a sensible first milestone. Deliver as a checklist the agent (or user) can execute item by item.

### Deploy / Ship
Before anything irreversible: establish the target (environment, service, pipeline) and check for existing listeners/processes/config that could conflict.

- **Preflight**: build passes, tests pass, migrations are compatible, config/secrets resolved, rollback path exists.
- **Deliverable**: a deployment plan — steps in execution order, the exact commands, a go/no-go checkpoint before anything touches production, and a rollback step for each mutation.
- **Never deploy to production without explicit user approval** of the plan; ask once, plainly. Dry-run or staging first when possible.
- If the user says just "ship it" and there is no deployable artifact, surface what's missing instead of guessing.

### Migrate
Data and schema changes are one-way doors — treat them that way.

- **Inventory** what moves: schema, data, code call-sites, docs, env vars, caches.
- **Plan for reversibility**: prefer additive changes (expand → migrate → contract), write the down-migration or rollback before the up, and never destroy data without a backup and explicit confirmation.
- **Execute in verifiable steps**: apply the change, verify with a real query/test on a small sample, then continue. Report what changed, what was verified, and any rows/files deliberately left alone.

### Optimize
"Optimize", "make it fast", "speed this up" — measure before touching anything.

- **Baseline**: benchmark or profile the current state and record the numbers (or state clearly why a qualitative baseline is all that's feasible).
- **Target**: identify the actual bottleneck from evidence, not folklore; state the suspected hot spot and expected gain before changing code.
- **Keep it honest**: prefer the minimal change that hits the goal; preserve correctness with tests; re-run the same benchmark after and report before/after. If the gain is marginal, say so and consider reverting.

### Secure
A security-focused pass over the target, stricter than an audit's security section.

- **Check systematically**: input validation and injection (SQL, command, XSS, path traversal), authn/authz gaps, secrets in code or logs, unsafe deserialization, dependency vulnerabilities, insecure defaults, missing rate limiting, and data exposure in errors or responses.
- **Output**: findings ranked by exploitability and impact, each with the attack scenario, a concrete fix, and what NOT to break while fixing it.
- **Fix nothing silently**: list findings first. For each fix, prefer the smallest hardening change; note behavioral changes (e.g., endpoints now rejecting previously accepted input).

## Rules

- **Preserve intent.** Expansion adds depth and structure; it never changes what the user asked for.
- **Show rewrites when explicitly asked.** If the message itself asks to improve a prompt ("upgrade this prompt"), present the upgraded prompt for review before executing. The silent expand-and-execute path is only for deliverable shorthand like "Audit this".
- **State assumptions.** One line up front: what "this" resolved to and which template was applied.
- **Always define the output format** before starting work, per the template.
- **Depth scales with scope.** Auditing one function ≠ auditing a repo; don't produce a 40-section report for a 30-line file.
- **If the user says "no, I meant simply X"**, drop the expansion and do exactly X.
