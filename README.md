# meta-skill-suite

[![Validate skill suite](https://github.com/Mixj73IT/meta-skill-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/Mixj73IT/meta-skill-suite/actions/workflows/validate.yml)

A **mode dial** for AI coding agents: three skills that scale what a single
terse message triggers — plus a router that routes, a self-tuning rule that
learns from your corrections, and a validator that keeps the whole thing
honest.

Built for [Codebuff](https://www.codebuff.com); works with any agent that
reads `.agents/skills/` (and with Claude Code via a `.claude/skills/` mirror).

## The dial

| Skill | Dials | Fire it with |
|---|---|---|
| `upgrade-prompt` | **scope up** | terse deliverables: "Audit this", "Fix this", "Deploy this" |
| `deep-dive` | **rigor up** | explicit depth: "deep dive", "don't hold back" |
| `quick-answer` | **ceremony down** | small factual questions: "TL;DR", "just tell me" |

Say **"Audit this"** and get a real audit: executive summary, severity-ranked
findings with file:line references, and a prioritized todo list. Modes layer
rather than compete — "deep-dive audit of this" is full scope at full rigor.

## How it fits together

- **`AGENTS.md`** routes messages to modes (deliverable verb first) and
  self-tunes: when you correct a routing choice, the correction is recorded
  as a rule so the router learns your defaults.
- Each skill's **Boundary** section is its routing contract — when it owns a
  message and when it defers.
- **`scripts/validate_skills.py`** enforces the contracts: frontmatter
  validity, router coverage in both directions, learned-row hygiene, and
  project/global sync. Runs locally and in CI on every push.

## Install

```bash
git clone https://github.com/Mixj73IT/meta-skill-suite
cp -r meta-skill-suite/.agents/skills/* ~/.agents/skills/   # global
# or copy into .agents/skills/ of a project
```

Restart Codebuff (or your agent) to load the skills. Each one is also a
slash command: `/skill:upgrade-prompt`, `/skill:deep-dive`, `/skill:quick-answer`.

## Validate

```bash
python scripts/validate_skills.py
```

Run after editing any skill or the router — it fails loudly on drift,
stale router rows, and broken contracts.

## License

[MIT](LICENSE)
