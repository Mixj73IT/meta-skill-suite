# Skills — the mode dial

Three orthogonal ways to scale what one message triggers. Codebuff loads these
from this directory (project-level); copy any of them to `~/.agents/skills/` to
have them in every project (Codebuff also reads `.claude/skills/`, so mirroring
there keeps the dial working in Claude Code too). Restart Codebuff after
changes.

| Skill | Dials | Fire it with |
|---|---|---|
| `upgrade-prompt` | **scope up** | terse deliverables: "Audit this", "Fix this", "Deploy this" |
| `deep-dive` | **rigor up** | explicit depth: "deep dive", "don't hold back"; high-stakes topics |
| `quick-answer` | **ceremony down** | small factual questions, "TL;DR", "just tell me" |

Routing is defined in the project-root `AGENTS.md` ("Response-mode routing"
table); each skill's **Boundary** section is its contract for when it owns a
message — keep both in agreement. Modes layer rather than compete:
"deep-dive audit of this" = upgrade-prompt's scope at deep-dive's rigor.
Corrections to a routing choice are recorded in `AGENTS.md`'s self-tuning rule,
so the router learns your defaults over time.

After editing anything here, run `python scripts/validate_skills.py`.
