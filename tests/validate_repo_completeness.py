#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_file(path: str) -> str:
    file_path = ROOT / path
    require(file_path.exists(), f"missing required file: {path}")
    return file_path.read_text(encoding="utf-8")


def main() -> None:
    license_text = require_file("LICENSE")
    require("MIT License" in license_text, "LICENSE must use MIT")
    require("heidashuai777" in license_text, "LICENSE must name the repository owner")

    workflow = require_file(".github/workflows/validate.yml")
    for command in [
        "python -B tests/validate_resource_scaffold.py",
        "python -B tests/validate_repo_completeness.py",
        "python -B -m unittest discover -s tests",
    ]:
        require(command in workflow, f"workflow missing command: {command}")

    metadata = require_file(".codex/skills/mathematica-codex-helper/agents/openai.yaml")
    for term in [
        'display_name: "Mathematica Codex Helper"',
        'short_description: "Manual-backed Wolfram and physics coding"',
        'default_prompt: "Use $mathematica-codex-helper',
        "allow_implicit_invocation: true",
    ]:
        require(term in metadata, f"openai.yaml missing term: {term}")

    changelog = require_file("CHANGELOG.md")
    require("## v0.3.0 - 2026-06-30" in changelog, "CHANGELOG must document v0.3.0")
    require("resource-aware" in changelog.lower(), "CHANGELOG must describe resource-aware changes")
    require("section/subsection" in changelog, "CHANGELOG must describe readability changes")

    contributing = require_file("CONTRIBUTING.md")
    require("python -B -m unittest discover -s tests" in contributing, "CONTRIBUTING must document tests")

    security = require_file("SECURITY.md")
    require("Do not report secrets in public issues" in security, "SECURITY must include private-reporting guidance")

    readme = read("README.md")
    for term in ["MIT", "v0.3.0", "Validation", "quiet diagnostics", "parallel execution"]:
        require(term in readme, f"README missing completion term: {term}")

    print("repo completeness validation passed")


if __name__ == "__main__":
    main()
