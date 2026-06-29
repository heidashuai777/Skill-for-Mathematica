# Skill for Mathematica

[![Validate](https://github.com/heidashuai777/Skill-for-Mathematica/actions/workflows/validate.yml/badge.svg)](https://github.com/heidashuai777/Skill-for-Mathematica/actions/workflows/validate.yml)

This repository contains a Codex skill for writing readable Mathematica / Wolfram Language code with stronger package accuracy, especially for physics packages.

Current release target: `v0.2.0`

License: MIT

The skill is located at:

```
.codex/skills/mathematica-codex-helper/SKILL.md
```

A lowercase copy is also included at:

```
.codex/skills/mathematica-codex-helper/skill.md
```

## What the skill enforces

- Human-readable Mathematica code.
- Clear mathematical derivations before code.
- Explicit physics conventions.
- Package usage grounded in manuals and examples.
- Minimal smoke tests before adapting package examples.
- Runtime or static validation when possible.

## Supporting references

```
.codex/skills/mathematica-codex-helper/references/manual-example-integration.md
.codex/skills/mathematica-codex-helper/references/wolfram-style-guide.md
.codex/skills/mathematica-codex-helper/references/physics-package-playbook.md
.codex/skills/mathematica-codex-helper/references/wolfram-resource-integration.md
```

## Typical requests

```
Use the Mathematica skill to write readable code for this physics derivation.
Use xAct, but first follow the manual examples and state the conventions.
Use FeynCalc for this gamma-matrix trace and include smoke tests.
Convert this derivation into a clear Mathematica notebook-style script.
```

## Recommended workflow for package-heavy tasks

1. Find the official package manual and examples.
2. Build a short package evidence card.
3. Run the smallest official example unchanged.
4. Adapt the example incrementally.
5. Add physics checks such as limits, symmetries, dimensions, and normalization.

## Using this skill

To use this skill in Codex:

1. In the Codex CLI, type `$` to open the skill manager.
2. Choose the option to **install a skill** and provide the URL of this repository.
3. Codex will download the `.codex/skills/mathematica-codex-helper` directory and register the skill automatically.
4. To invoke the skill manually, run `$mathematica-codex-helper` in the Codex CLI when you want help with Mathematica or physics-related tasks.
5. You can also rely on automatic triggers: the skill will be loaded automatically when your prompt matches one of the triggers defined in `SKILL.md`.
6. Make sure you’re working within this repository or have installed the skill globally so Codex knows where to find it.

## Wolfram resource integration

This repo now includes a resource-aware scaffold for grounding the skill in official Wolfram resources:

- **Wolfram Prompt Repository** candidates for sample code, reformatting, comments, documentation, naming suggestions, and answer assessment.
- **Wolfram Example Repository** candidates for verified example-memory, tool-mediated lookup, and reranking patterns.
- A structured manifest at `data/wolfram-resource-manifest.json`.
- Offline helper scripts at `scripts/wolfram_resource_lookup.py` and `scripts/extract_wl_examples.py`.
- A detailed playbook at `.codex/skills/mathematica-codex-helper/references/wolfram-resource-integration.md`.

### Supported integration modes

1. **Docs-only mode**
   - Uses `SKILL.md` and the static `references/` files.
   - Requires no Wolfram account, network access, or credentials.
   - Remains the safe fallback whenever live resources are unavailable.

2. **Resource-aware mode**
   - Uses the manifest to route tasks to candidate Wolfram prompts or example patterns.
   - Recommended for package-heavy, physics-heavy, code transformation, naming, and documentation tasks.
   - Requires verification before claiming that a named prompt or example was used.

3. **Strict validation mode**
   - Adds an evidence card, smoke test, mathematical or physical sanity check, and uncertainty note.
   - Recommended when answers depend on unfamiliar Wolfram package APIs or version-sensitive workflows.

### Recommended resource-aware workflow

When a task depends on nontrivial Wolfram Language package usage:

1. Identify the relevant Wolfram prompt or example candidate from the manifest.
2. Verify the resource through local documentation, installed Wolfram tooling, or live Wolfram access when available.
3. Build a short evidence card with source checked, minimal example, adaptation map, smoke test, conventions, and remaining uncertainty.
4. Generate the answer only from verified patterns.
5. Report one validation check in the final answer.

You can query the local manifest without network access:

```bash
python scripts/wolfram_resource_lookup.py --kind prompts --query "add comments to Mathematica code"
python scripts/wolfram_resource_lookup.py --kind examples --query "rerank semantic search snippets"
```

The helper returns candidate resources only. Verify live Wolfram availability before citing a prompt or example as evidence.

You can also extract local Wolfram examples into JSONL:

```bash
python scripts/extract_wl_examples.py README.md Documentation/ Examples/ --output artifacts/verified-example-snippets.jsonl
```

The extractor handles fenced Markdown examples and whole `.wl` / `.m` files. It does not parse notebooks directly.

### Credentials and security

Live Wolfram-backed features may require a Wolfram account, internet access, LLM-enabled Wolfram functionality, or secure local credentials.

Never commit credentials to this repository. Use environment variables, OS keychain storage, Wolfram secure credential mechanisms, or another local secret manager.

### Cache and manifests

Suggested future local files:

```
data/wolfram-resource-manifest.json
artifacts/verified-example-snippets.jsonl
artifacts/semantic-index/
```

Cache only public metadata or user-approved snippets. Do not cache secrets, private notebooks, proprietary package docs, or unpublished research code unless explicitly requested.

## Validation

Run the local validation suite before publishing changes:

```bash
python -B tests/validate_resource_scaffold.py
python -B tests/validate_repo_completeness.py
python -B -m unittest discover -s tests
python -B -c "import json; json.load(open('data/wolfram-resource-manifest.json', encoding='utf-8')); print('json ok')"
diff -q .codex/skills/mathematica-codex-helper/SKILL.md .codex/skills/mathematica-codex-helper/skill.md
```

GitHub Actions runs the same deterministic checks without requiring Wolfram credentials.

## Release

`v0.2.0` is the resource-aware scaffold release. It adds Wolfram resource routing, helper scripts, validation, CI, and repository metadata while keeping docs-only mode available.
