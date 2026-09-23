#!/usr/bin/env python3
"""Small distribution checks. Not a Wolfram parser or runtime test."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/mathematica-codex-helper"
REQUIRED = (
    "SKILL.md",
    "references/wolfram-style-guide.md",
    "references/interactive-workflow.md",
    "references/economy.md",
    "references/parallel-runtime.md",
    "references/manual-example-integration.md",
    "references/physics-package-playbook.md",
    "examples/gaussian-ground-state.wl",
)


def wl_balance(text: str) -> None:
    """Check delimiters, quoted strings and nested comments; no evaluation."""
    stack: list[str] = []
    comments = 0
    quoted = False
    i = 0
    pairs = {")": "(", "]": "[", "}": "{", "|>": "<|"}
    while i < len(text):
        pair = text[i:i + 2]
        char = text[i]
        if comments:
            if pair == "(*":
                comments += 1
                i += 2
            elif pair == "*)":
                comments -= 1
                i += 2
            else:
                i += 1
            continue
        if quoted:
            if char == "\\":
                i += 2
            else:
                quoted = char != '"'
                i += 1
            continue
        if pair == "(*":
            comments = 1
            i += 2
        elif char == '"':
            quoted = True
            i += 1
        elif pair == "<|":
            stack.append(pair)
            i += 2
        elif pair == "|>" or char in ")]}":
            token = pair if pair == "|>" else char
            if not stack or stack.pop() != pairs[token]:
                raise ValueError(f"unbalanced delimiter at character {i}")
            i += len(token)
        elif char in "([{":
            stack.append(char)
            i += 1
        elif pair == "*)":
            raise ValueError(f"unmatched comment end at character {i}")
        else:
            i += 1
    if stack or comments or quoted:
        raise ValueError("unclosed delimiter, comment or string")


def prose_without_fences(text: str) -> str:
    """Validate simple fenced blocks and return prose for local-link checks."""
    fence: str | None = None
    prose: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if fence is None:
            if match:
                fence = match.group(1)
            else:
                prose.append(line)
        elif (match and match.group(1)[0] == fence[0]
              and len(match.group(1)) >= len(fence)
              and not match.group(2).strip()):
            fence = None
    if fence:
        raise ValueError("unclosed Markdown code fence")
    return "\n".join(prose)


def check_markdown(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"turn\d+(?:file|view|search)\d+||〖turn", text):
        raise ValueError("conversation-specific citation marker")
    prose = prose_without_fences(text)
    # This repository deliberately uses simple inline Markdown links only.
    for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", prose):
        parts = urlsplit(target.strip("<>"))
        if parts.scheme or parts.netloc or not parts.path:
            continue
        destination = (path.parent / unquote(parts.path)).resolve()
        try:
            destination.relative_to(ROOT)
        except ValueError as exc:
            raise ValueError(f"local link escapes repository: {target}") from exc
        if not destination.exists():
            raise ValueError(f"missing local link: {target}")


def self_test() -> None:
    good = [
        'f["[not a bracket]", <|"a" -> {1, 2}|>]',
        '(* nested (* ] *) comment *) f[(x + 1)]',
        r'f["escaped \" quote"]',
        'expr[[1]]; (* valid Part delimiters *)',
    ]
    bad = ['f[{1)]', '(* unfinished', 'f["unfinished]', '<|"a"->1}', '*)']
    for text in good:
        wl_balance(text)
    for text in bad:
        try:
            wl_balance(text)
        except ValueError:
            continue
        raise ValueError(f"lexical self-test failed: {text!r}")
    prose_without_fences('text\n```wl\nf[x]\n```\nend')
    try:
        prose_without_fences('```wl\nf[x]')
    except ValueError:
        return
    raise ValueError("fence self-test failed")


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (SKILL / relative).is_file():
            errors.append(f"missing {relative}")
    definitions = [
        path for root in (ROOT / ".agents/skills", ROOT / ".codex/skills")
        if root.exists() for path in root.rglob("*")
        if path.is_file() and path.name.lower() == "skill.md"
    ]
    if definitions != [SKILL / "SKILL.md"]:
        errors.append("expected exactly one uppercase canonical skill definition")
    core = SKILL / "SKILL.md"
    words = 0
    if core.is_file():
        text = core.read_text(encoding="utf-8")
        words = len(text.split())
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not front or not re.search(
            r"^name: mathematica-codex-helper$", front.group(1), re.M
        ) or not re.search(r"^description: \S.+$", front.group(1), re.M):
            errors.append("missing expected name/description front matter")
        if "references/parallel-runtime.md" not in text:
            errors.append("missing core link to the shared parallel-runtime policy")
        if words > 850:
            errors.append(f"core exceeds the 850-word maintenance budget: {words}")
    for path in [ROOT / "README.md", ROOT / "AGENTS.md", *SKILL.rglob("*.md")]:
        try:
            check_markdown(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    for path in SKILL.rglob("*.wl"):
        try:
            source = path.read_text(encoding="utf-8")
            wl_balance(source)
            if "(* ::Section:: *)" not in source:
                raise ValueError("worked example needs mathematical sections")
            if re.search(r"\bPrint\s*\[|\(\*\s*Summary\s*\*\)", source):
                raise ValueError("worked example contains routine narration/summary")
        except (OSError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    try:
        self_test()
    except ValueError as exc:
        errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: structure, local links, fences and lexical checks; core {words} words.")
    print("Wolfram execution and physics/package validation were NOT performed by this test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
