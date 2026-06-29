#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TextIO

WL_EXTENSIONS = {".wl", ".m"}
MARKDOWN_EXTENSIONS = {".md", ".markdown"}
WL_FENCE_LANGUAGES = {"mathematica", "wolfram", "wolframlanguage", "wl", "mma"}

FENCE_RE = re.compile(
    r"(?P<fence>```|~~~)[ \t]*(?P<language>[A-Za-z0-9_-]+)?[^\n]*\n"
    r"(?P<code>.*?)"
    r"(?P=fence)",
    re.DOTALL,
)


def iter_input_files(paths: Iterable[Path]) -> Iterator[Path]:
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and is_supported_file(child):
                    yield child
        elif path.is_file() and is_supported_file(path):
            yield path


def is_supported_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    return suffix in WL_EXTENSIONS or suffix in MARKDOWN_EXTENSIONS


def normalized_language(language: str | None) -> str:
    return (language or "").strip().lower()


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_markdown_examples(path: Path) -> Iterator[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    for match in FENCE_RE.finditer(text):
        language = normalized_language(match.group("language"))
        if language not in WL_FENCE_LANGUAGES:
            continue
        code = match.group("code").strip("\n")
        if not code.strip():
            continue
        yield {
            "source_path": str(path),
            "source_type": "markdown-fence",
            "language": language,
            "start_line": line_number_for_offset(text, match.start("code")),
            "code": code,
        }


def extract_wolfram_file(path: Path) -> Iterator[dict[str, object]]:
    code = path.read_text(encoding="utf-8").strip("\n")
    if not code.strip():
        return
    yield {
        "source_path": str(path),
        "source_type": "wolfram-file",
        "language": path.suffix.lower().lstrip("."),
        "start_line": 1,
        "code": code,
    }


def collect_examples(paths: Iterable[Path]) -> Iterator[dict[str, object]]:
    for path in iter_input_files(paths):
        suffix = path.suffix.lower()
        if suffix in MARKDOWN_EXTENSIONS:
            yield from extract_markdown_examples(path)
        elif suffix in WL_EXTENSIONS:
            yield from extract_wolfram_file(path)


def write_jsonl(examples: Iterable[dict[str, object]], output: TextIO) -> None:
    for example in examples:
        output.write(json.dumps(example, ensure_ascii=False, sort_keys=True) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract fenced Wolfram Language examples from Markdown and whole .wl/.m files into JSONL."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Files or directories to scan.")
    parser.add_argument("--output", type=Path, help="JSONL output path. Defaults to stdout.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    examples = list(collect_examples(args.paths))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as output:
            write_jsonl(examples, output)
    else:
        write_jsonl(examples, sys.stdout)


if __name__ == "__main__":
    main()
