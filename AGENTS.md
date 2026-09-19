# Agent Rules

## Response-mode routing (the mode dial)

Three skills form a dial for how much work one message should trigger. Route by the
message's **deliverable verb first, then explicit depth words** — when two modes
plausibly apply, the verb wins over the adverb.

| Mode | Skill | Owns the message when | Defers when |
|------|-------|----------------------|-------------|
| **Upgrade** | `/skill:upgrade-prompt` | Bare imperative or <~8-word shorthand with a deliverable verb (audit, fix, review, build, deploy…) | Message already has specifics (just work); small factual question |
| **Deep** | `/skill:deep-dive` | Explicit depth ("deep dive", "go deep", "don't hold back") or high stakes (incident, security, architecture) | Small factual question; bare imperative without depth words |
| **Quick** | `/skill:quick-answer` | Small factual question or explicit brevity ("TL;DR", "quickly", "just tell me") | Any deliverable verb present |

How the modes combine:

1. Route before answering, and say which mode you chose in one short line.
2. Modes layer rather than compete: scope from upgrade-prompt, rigor from deep-dive,
   delivery style from quick-answer. ("Deep-dive audit of this" = upgrade-prompt's
   scope + deep-dive's rigor.)
3. No mode fits → answer normally. Don't force one.

Each skill's "Boundary" section is the contract for when it owns a message; keep
this table and those sections in agreement.

### Self-tuning: corrections update this table

When the user corrects a routing choice — "no, I meant the short version",
"next time just do it", "I wanted the deep version of that" — that correction is
a routing rule, not just a one-off. Record it in this file so the router learns
their defaults:

1. **Classify the correction.** What did the user actually want — a different
   mode (quick instead of upgrade), a layering change (deep + upgrade), or an
   exception for a specific phrase or target ("'audit' means the security
   audit only")?
2. **Amend this file.** Adjust the owning row's "Owns/Defers" cells, or add a
   one-line example row for the phrase under the table. Keep each row's
   trigger/defer wording short and pattern-like so it generalizes — write rules,
   not transcripts.
3. **Mirror into the skill.** If the correction tightens when a skill owns or
   defers a message, update that skill's Boundary section in the same pass
   (and vice versa: skill-side corrections flow back here).
4. **Confirm in one line** — e.g. "Noted: 'quick' + deliverable verbs still
   routes to upgrade-prompt, just faster." Then re-run the affected work in the
   corrected mode when it makes sense.

Don't wait for corrections to be explicit — if the user overrides a mode choice,
that's the same signal. And cap it: distinct rules only, merge near-duplicates,
prune rules that stop matching how they actually talk.

## Maintenance

After adding or editing anything in `.agents/skills/` or this file, run
`python scripts/validate_skills.py` — it checks frontmatter validity, router
coverage in both directions, self-tuning table hygiene, and that the global
copies in `~/.agents/skills/` are in sync — then restart Codebuff to reload
skills.
