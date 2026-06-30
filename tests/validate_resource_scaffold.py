#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".codex" / "skills" / "mathematica-codex-helper"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    skill = SKILL_DIR / "SKILL.md"
    lower_skill = SKILL_DIR / "skill.md"
    reference = SKILL_DIR / "references" / "wolfram-resource-integration.md"
    manifest = ROOT / "data" / "wolfram-resource-manifest.json"
    lookup_script = ROOT / "scripts" / "wolfram_resource_lookup.py"
    extract_script = ROOT / "scripts" / "extract_wl_examples.py"
    readme = ROOT / "README.md"

    for path in [skill, lower_skill, reference, manifest, lookup_script, extract_script, readme]:
        require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")

    skill_text = read(skill)
    lower_text = read(lower_skill)
    require(skill_text == lower_text, "SKILL.md and skill.md must stay synchronized")

    required_skill_terms = [
        "Wolfram resource routing",
        "Wolfram Prompt Repository",
        "Wolfram Example Repository",
        "Resource-aware workflow",
        "Fail closed",
        "wolfram-resource-integration.md",
        "sectioned scripts",
        "quiet logging",
        "main calculation",
        "verification",
    ]
    for term in required_skill_terms:
        require(term in skill_text, f"missing skill routing term: {term}")

    reference_text = read(reference)
    required_reference_terms = [
        "Docs-only mode",
        "Resource-aware mode",
        "Strict validation mode",
        "Credentials and security",
        "Cache policy",
        "No secrets",
    ]
    for term in required_reference_terms:
        require(term in reference_text, f"missing reference term: {term}")

    style_reference = SKILL_DIR / "references" / "wolfram-style-guide.md"
    style_text = read(style_reference)
    required_style_terms = [
        "Sectioning Template",
        "::Section::",
        "::Subsection::",
        "quietLog",
        "SetDirectory",
        "Print",
        "ParallelMap",
        "TimeConstrained",
        "Package Conflict Safety",
        "Result Simplification Loop",
        "Main Calculation vs Verification",
    ]
    for term in required_style_terms:
        require(term in style_text, f"missing style-guide term: {term}")

    wolfram_doc_urls = [
        "https://reference.wolfram.com/language/ref/Needs.html",
        "https://reference.wolfram.com/language/ref/BeginPackage.html",
        "https://reference.wolfram.com/language/ref/ParallelMap.html",
        "https://reference.wolfram.com/language/ref/FullSimplify.html",
        "https://reference.wolfram.com/language/ref/TimeConstrained.html",
        "https://reference.wolfram.com/language/ref/Message.html",
        "https://reference.wolfram.com/language/ref/Echo.html",
    ]
    for url in wolfram_doc_urls:
        require(url in style_text, f"missing Wolfram documentation URL: {url}")

    readme_text = read(readme)
    for term in ["Wolfram resource integration", "Resource-aware mode", "Strict validation mode"]:
        require(term in readme_text, f"missing README term: {term}")

    manifest_data = json.loads(read(manifest))
    prompt_names = {item["name"] for item in manifest_data["prompts"]}
    example_names = {item["name"] for item in manifest_data["examples"]}

    for name in [
        "WolframSampleCode",
        "CodeReformat",
        "CodeCommentInsert",
        "CodeDocAnnotator",
        "FunctionNameSuggest",
        "VariableNameSuggest",
        "LLMPromptAssessment",
    ]:
        require(name in prompt_names, f"missing prompt manifest entry: {name}")

    for name in [
        "Generate Email Replies with a Semantic Search Memory",
        "Provide Socioeconomic Data with an LLM Tool to Avoid Hallucinations",
        "Re-ranking Text Matches in Semantic Search Queries",
    ]:
        require(name in example_names, f"missing example manifest entry: {name}")

    checklist = manifest_data["validation"]["required_evidence_fields"]
    for field in ["source_checked", "minimal_example", "adaptation_map", "smoke_test", "remaining_uncertainty"]:
        require(field in checklist, f"missing validation field: {field}")

    print("resource-aware scaffold validation passed")


if __name__ == "__main__":
    main()
