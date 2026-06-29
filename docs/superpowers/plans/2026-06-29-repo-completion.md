# Repo Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the public packaging around the Mathematica Codex Helper skill.

**Architecture:** Add repo-level metadata and deterministic validation without changing the skill's runtime model. CI runs local Python and file-contract checks only.

**Tech Stack:** Markdown, YAML, Python standard library, GitHub Actions.

---

### Task 1: Add Completion Validation

**Files:**
- Create: `tests/validate_repo_completeness.py`

- [ ] Add a Python script that checks for `LICENSE`, `.github/workflows/validate.yml`, `agents/openai.yaml`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, and README release/license/validation terms.
- [ ] Run `python -B tests/validate_repo_completeness.py` and confirm it fails before the completion files exist.

### Task 2: Add Repo Metadata

**Files:**
- Create: `LICENSE`
- Create: `CHANGELOG.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `.codex/skills/mathematica-codex-helper/agents/openai.yaml`

- [ ] Add MIT license text for `heidashuai777`.
- [ ] Add `v0.2.0` changelog notes.
- [ ] Add contribution and security guidance.
- [ ] Add skill UI metadata with `display_name`, `short_description`, `default_prompt`, and implicit invocation policy.

### Task 3: Add CI

**Files:**
- Create: `.github/workflows/validate.yml`

- [ ] Add a `Validate` workflow for pull requests and pushes to `main` / `codex/**`.
- [ ] Run scaffold validation, repo completeness validation, unit tests, JSON parse, and skill sync checks.

### Task 4: Update README

**Files:**
- Modify: `README.md`

- [ ] Add CI badge, current release, license, validation commands, and release guidance.

### Task 5: Verify and Publish

**Commands:**

```bash
python -B tests/validate_resource_scaffold.py
python -B tests/validate_repo_completeness.py
python -B -m unittest discover -s tests
python -B -c "import json; json.load(open('data/wolfram-resource-manifest.json', encoding='utf-8')); print('json ok')"
diff -q .codex/skills/mathematica-codex-helper/SKILL.md .codex/skills/mathematica-codex-helper/skill.md
```

- [ ] Commit and push the completion update to PR #1.
- [ ] Mark PR #1 ready for review.
- [ ] Merge PR #1 to `main`.
- [ ] Create GitHub release `v0.2.0`.
