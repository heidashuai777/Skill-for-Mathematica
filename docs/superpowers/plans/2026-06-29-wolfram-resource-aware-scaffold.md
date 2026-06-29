# Wolfram Resource-Aware Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a resource-aware Wolfram Prompt/Example Repository scaffold to the Mathematica Codex Helper skill.

**Architecture:** Keep the skill Markdown as the policy layer, add one focused reference document as the operational playbook, add one JSON manifest as structured resource inventory, add offline helpers for manifest ranking and Wolfram example extraction, and validate the contract with Python scripts. This pass does not add live Wolfram retrieval or semantic search.

**Tech Stack:** Markdown, JSON, Python standard library.

---

## File Structure

- `README.md`: user-facing setup and usage documentation.
- `.codex/skills/mathematica-codex-helper/SKILL.md`: primary skill entrypoint and resource routing.
- `.codex/skills/mathematica-codex-helper/skill.md`: lowercase synchronized copy.
- `.codex/skills/mathematica-codex-helper/references/wolfram-resource-integration.md`: detailed resource-aware playbook.
- `data/wolfram-resource-manifest.json`: structured prompt/example inventory and validation checklist.
- `scripts/wolfram_resource_lookup.py`: offline manifest lookup and query ranking helper.
- `scripts/extract_wl_examples.py`: extracts fenced Wolfram Language Markdown examples and `.wl`/`.m` files into JSONL.
- `.gitignore`: excludes generated artifacts and Python bytecode.
- `tests/validate_resource_scaffold.py`: structure-first validation.
- `tests/test_wolfram_resource_lookup.py`: behavior tests for lookup ranking and CLI JSON output.
- `tests/test_extract_wl_examples.py`: behavior tests for extraction and JSONL output.

### Task 1: Add Failing Scaffold Validation

**Files:**
- Create: `tests/validate_resource_scaffold.py`

- [ ] **Step 1: Write validation script**

```python
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
    readme = ROOT / "README.md"

    for path in [skill, lower_skill, reference, manifest, readme]:
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
```

- [ ] **Step 2: Run validation and verify RED**

Run: `python tests/validate_resource_scaffold.py`

Expected: FAIL before implementation, with a missing reference or manifest assertion.

### Task 2: Add Manifest and Reference Playbook

**Files:**
- Create: `data/wolfram-resource-manifest.json`
- Create: `.codex/skills/mathematica-codex-helper/references/wolfram-resource-integration.md`

- [ ] **Step 1: Add `data/wolfram-resource-manifest.json`**

Use JSON with top-level `schema_version`, `modes`, `prompts`, `examples`, and `validation` fields. Include the seven prompt names and three example names from the design spec.

- [ ] **Step 2: Add `wolfram-resource-integration.md`**

Document docs-only mode, resource-aware mode, strict validation mode, routing rules, credential/security rules, cache policy, and fail-closed behavior.

### Task 3: Upgrade Skill Entry Points

**Files:**
- Modify: `.codex/skills/mathematica-codex-helper/SKILL.md`
- Modify: `.codex/skills/mathematica-codex-helper/skill.md`

- [ ] **Step 1: Update `SKILL.md`**

Add concise sections for Wolfram resource routing, resource-aware workflow, strict validation, and when to read the new reference file.

- [ ] **Step 2: Synchronize lowercase copy**

Make `skill.md` byte-for-byte identical to `SKILL.md`.

### Task 4: Update README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add resource integration docs**

Add a `Wolfram resource integration` section covering docs-only mode, resource-aware mode, strict validation mode, credentials, and cache/manifests.

### Task 5: Verify

**Files:**
- Run: `python tests/validate_resource_scaffold.py`
- Run: `python tests/test_wolfram_resource_lookup.py`
- Run: `python tests/test_extract_wl_examples.py`
- Run: `git status --short`

- [ ] **Step 1: Run scaffold validation**

Expected: `resource-aware scaffold validation passed`

- [ ] **Step 2: Inspect git status**

Expected: only intended files are modified or added.
