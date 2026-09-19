#!/usr/bin/env python3
"""Validate the meta-skill suite.

Checks:
  1. Frontmatter  -- every skill parses; name matches directory; rules obeyed.
  2. Router       -- AGENTS.md's mode table covers every installed skill, with
                     no stale /skill: mentions; learned rows stay capped and
                     cite real skills or modes.
  3. Boundary     -- skills that reference siblings are referenced back.
  4. Sync         -- project skills match the global copies in ~/.agents/skills/.

Exit code 0 = healthy, 1 = problems found. Run after editing anything under
.agents/skills/ or AGENTS.md (see AGENTS.md -> Maintenance).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_SKILLS = Path(".agents/skills")
GLOBAL_SKILLS = Path.home() / ".agents" / "skills"
ROUTER = Path("AGENTS.md")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MENTION_RE = re.compile(r"/skill:([a-z0-9][a-z0-9-]*)")
SEP_ROW_RE = re.compile(r"^\s*\|[-\s:|]+\|?\s*$")
MODE_LABELS = ("Upgrade", "Deep", "Quick")
CUSTOM_ROW_CAP = 10


def fail(msg: str) -> int:
    print(f"  FAIL  {msg}")
    return 1


def ok(msg: str) -> int:
    print(f"  ok    {msg}")
    return 0


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None, "no frontmatter block"
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, None


def check_skill(path: Path, all_names: list[str]) -> int:
    problems = 0
    skill_md = path / "SKILL.md"
    rel = str(skill_md)
    fm, err = parse_frontmatter(skill_md)
    if fm is None:
        return fail(f"{rel}: {err}")
    text = skill_md.read_text(encoding="utf-8")

    name = fm.get("name", "")
    if not name:
        problems += fail(f"{rel}: missing 'name'")
    elif not (NAME_RE.match(name) and 1 <= len(name) <= 64):
        problems += fail(f"{rel}: invalid name {name!r}")
    elif name != path.name:
        problems += fail(f"{rel}: name {name!r} != directory {path.name!r}")
    else:
        problems += ok(f"{rel}: name {name!r} valid")

    desc = fm.get("description", "")
    if not 1 <= len(desc) <= 1024:
        problems += fail(f"{rel}: description must be 1-1024 chars")
    else:
        problems += ok(f"{rel}: description {len(desc)} chars")

    if not re.search(r"^## Boundary", text, re.M):
        problems += fail(f"{rel}: missing '## Boundary' section (router contract)")
    else:
        problems += ok(f"{rel}: boundary contract present")

    for other in all_names:
        if other != name and re.search(rf"\b{re.escape(other)}\b", text):
            other_text = (PROJECT_SKILLS / other / "SKILL.md").read_text(encoding="utf-8")
            if not re.search(rf"\b{re.escape(name)}\b", other_text):
                problems += fail(f"{rel}: references {other!r} but is not referenced back")
    return problems


def check_router(names: list[str]) -> int:
    if not ROUTER.exists():
        return fail("AGENTS.md missing -- router cannot cover skills")
    text = ROUTER.read_text(encoding="utf-8")
    problems = 0
    for name in names:
        if f"/skill:{name}" in text:
            problems += ok(f"router covers {name!r}")
        else:
            problems += fail(f"router does not mention /skill:{name}")
    return problems


def check_router_reverse(names: list[str]) -> int:
    """Every /skill: mention in AGENTS.md must point at an existing skill."""
    text = ROUTER.read_text(encoding="utf-8")
    mentioned = sorted(set(MENTION_RE.findall(text)))
    if not mentioned:
        return fail("router contains no /skill: mentions")
    problems = 0
    for name in mentioned:
        if name in names:
            problems += ok(f"router mention /skill:{name} resolves")
        else:
            problems += fail(f"router mentions /skill:{name} but no such skill exists (stale row?)")
    return problems


def check_self_tuning(names: list[str]) -> int:
    """Self-tuning hygiene: base table intact, learned rows capped and resolvable."""
    text = ROUTER.read_text(encoding="utf-8")
    if "### Self-tuning" not in text:
        return fail("AGENTS.md missing Self-tuning section")
    routing = text.split("### Self-tuning")[0]
    data_rows = [
        line
        for line in routing.splitlines()
        if line.strip().startswith("|") and "Mode" not in line and not SEP_ROW_RE.match(line)
    ]
    if len(data_rows) < len(MODE_LABELS):
        return fail(
            f"mode table has {len(data_rows)} data row(s); expected at least {len(MODE_LABELS)}"
        )
    custom = data_rows[len(MODE_LABELS):]
    problems = 0
    if len(custom) > CUSTOM_ROW_CAP:
        problems += fail(f"{len(custom)} learned rows exceeds cap of {CUSTOM_ROW_CAP} -- prune near-duplicates")
    for row in custom:
        resolves = any(
            f"/skill:{n}" in row or re.search(rf"\b{re.escape(n)}\b", row) for n in names
        ) or any(f"**{m}**" in row for m in MODE_LABELS)
        if resolves:
            problems += ok(f"learned row ok: {row.strip()[:52]!r}")
        else:
            problems += fail(f"learned row cites no known skill or mode: {row.strip()[:52]!r}")
    if not custom:
        problems += ok("no learned rows yet (base table only)")
    return problems


def check_sync(names: list[str]) -> int:
    problems = 0
    if not GLOBAL_SKILLS.is_dir():
        return fail(f"{GLOBAL_SKILLS} does not exist -- global install missing")
    for name in names:
        src = (PROJECT_SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
        dst = GLOBAL_SKILLS / name / "SKILL.md"
        if not dst.exists():
            problems += fail(f"global missing: {name}")
        elif dst.read_text(encoding="utf-8") != src:
            problems += fail(f"global out of sync: {name} (re-copy from project)")
        else:
            problems += ok(f"global in sync: {name}")
    return problems


def main() -> int:
    if not PROJECT_SKILLS.is_dir():
        print(f"no {PROJECT_SKILLS} -- nothing to validate")
        return 0
    skills = sorted(p for p in PROJECT_SKILLS.iterdir() if (p / "SKILL.md").is_file())
    names = [p.name for p in skills]
    print(f"Validating {len(names)} skill(s): {', '.join(names)}\n")
    problems = 0
    for path in skills:
        problems += check_skill(path, names)
        print()
    problems += check_router(names)
    print()
    problems += check_router_reverse(names)
    print()
    problems += check_self_tuning(names)
    print()
    problems += check_sync(names)
    print()
    if problems:
        print(f"{problems} problem(s) found.")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
