# Wolfram Resource-Aware Scaffold Design

## Goal

Upgrade `mathematica-codex-helper` from a policy-only skill into a resource-aware scaffold that can guide future Codex runs toward official Wolfram prompts, examples, evidence cards, and strict validation without requiring live Wolfram integration in this pass.

## Scope

This pass implements option 2 from the approved upgrade path:

- Add explicit Wolfram Prompt Repository and Wolfram Example Repository routing rules to the skill.
- Add a focused reference document for resource-aware modes, manifests, credentials, cache hygiene, and fail-closed behavior.
- Add a machine-readable manifest of known prompt/example resources and validation expectations.
- Add an offline lookup helper that ranks manifest entries for a user query without claiming live Wolfram verification.
- Add the missing Wolfram example extraction helper already referenced by the manual/example protocol.
- Add structure-first validation tests for the scaffold.
- Update `README.md` with setup, modes, credentials, and security notes.
- Ignore generated caches and Python bytecode.
- Keep `SKILL.md` and `skill.md` synchronized.

This pass does not implement a full semantic index, reranker, live Wolfram fetcher, or CI workflow. Those remain future work after the scaffold is stable.

## Architecture

The upgrade has three layers:

1. `SKILL.md` and `skill.md` remain the trigger and policy layer. They tell Codex when to use resource-aware behavior, when to load the new reference, and what evidence must appear in final answers.
2. `references/wolfram-resource-integration.md` is the operational playbook. It records modes, prompt/example routing, strict validation, credential rules, cache policy, and fallback behavior.
3. `data/wolfram-resource-manifest.json` is the structured resource inventory. It lists supported Wolfram prompt names, example names, usage roles, and the validation checklist that tests can enforce.
4. `scripts/wolfram_resource_lookup.py` is an offline helper for listing and ranking manifest entries. It never performs live Wolfram lookup and must label its output as offline manifest guidance.
5. `scripts/extract_wl_examples.py` extracts fenced Wolfram Language examples from Markdown and whole `.wl`/`.m` files into JSONL for future evidence caches.

The validation script checks the contract between those layers instead of exact prose. It confirms that required files exist, synchronized skill files match, the manifest parses, and the docs mention the resource-aware workflow and security boundaries.

## Files

- Modify `README.md`: document resource-aware mode, strict mode, credentials, manifests, and cache hygiene.
- Modify `.codex/skills/mathematica-codex-helper/SKILL.md`: add resource routing, fail-closed rules, and reference navigation.
- Modify `.codex/skills/mathematica-codex-helper/skill.md`: keep a synchronized lowercase copy.
- Add `.codex/skills/mathematica-codex-helper/references/wolfram-resource-integration.md`: detailed playbook.
- Add `data/wolfram-resource-manifest.json`: prompt/example/resource validation inventory.
- Add `scripts/wolfram_resource_lookup.py`: offline prompt/example manifest lookup helper.
- Add `scripts/extract_wl_examples.py`: Markdown and source-file Wolfram Language example extractor.
- Add `.gitignore`: ignore generated artifacts and Python cache files.
- Add `tests/validate_resource_scaffold.py`: structure-first validation checks.
- Add `tests/test_wolfram_resource_lookup.py`: behavior checks for lookup ranking and CLI JSON output.
- Add `tests/test_extract_wl_examples.py`: behavior checks for example extraction and JSONL output.

## Success Criteria

- `python tests/validate_resource_scaffold.py` exits with status 0.
- The validation test fails on the pre-upgrade state because the required resource-aware scaffold is missing.
- `SKILL.md` and `skill.md` are byte-for-byte identical after implementation.
- `python tests/test_wolfram_resource_lookup.py` exits with status 0.
- `python tests/test_extract_wl_examples.py` exits with status 0.
- The README explains docs-only, resource-aware, and strict validation modes.
- No secrets, credentials, generated caches, or live Wolfram artifacts are committed.

## Risks

- Prompt or example names may change upstream. The manifest must fail closed and mark resources as candidates, not guaranteed live availability.
- Some users will not have Wolfram LLM credentials. Docs-only mode must remain a valid fallback.
- Overloading `SKILL.md` would make the skill harder to load. Detailed operational rules belong in the new reference file.
