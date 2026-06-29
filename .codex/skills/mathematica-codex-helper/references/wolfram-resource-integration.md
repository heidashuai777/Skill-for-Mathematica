# Wolfram Resource Integration

Use this reference when a Mathematica or Wolfram Language task benefits from named Wolfram prompts, verified example notebooks, or strict evidence tracking. Keep the main skill concise; load this file for package-heavy, physics-heavy, code-transformation, documentation, naming, or hallucination-risk tasks.

## Docs-only mode

Use Docs-only mode when live Wolfram access is unavailable, unnecessary, or outside the user's requested scope.

- Use `SKILL.md`, `manual-example-integration.md`, `wolfram-style-guide.md`, and `physics-package-playbook.md`.
- Prefer official documentation, installed paclet docs, local examples, and user-provided source over memory.
- State when no live Wolfram Prompt Repository or Wolfram Example Repository lookup was performed.
- Keep evidence cards short and precise.

## Resource-aware mode

Use Resource-aware mode when named Wolfram resources can improve correctness or consistency.

Route tasks this way:

| User need | Candidate Wolfram resource | Expected use |
| --- | --- | --- |
| Short canonical usage pattern | `WolframSampleCode` | Start from a verified short example before elaborating. |
| Reformat or clean existing code | `CodeReformat` | Preserve semantics while improving structure. |
| Add useful comments | `CodeCommentInsert` | Explain intent and mathematical meaning, not obvious syntax. |
| Generate package documentation | `CodeDocAnnotator` | Draft `::usage`, syntax notes, and examples for package functions. |
| Improve function names | `FunctionNameSuggest` | Suggest readable API names compatible with Wolfram conventions. |
| Improve variable names | `VariableNameSuggest` | Suggest descriptive notebook or package variable names. |
| Assess an answer | `LLMPromptAssessment` | Check evidence, conventions, hallucinated symbols, and validation coverage. |

For example-oriented work, treat Wolfram Example Repository entries as reusable patterns, not as text to copy wholesale. Use example notebooks to identify setup order, resource access patterns, retrieval architecture, and validation ideas.

## Strict validation mode

Use Strict validation mode when:

- the user asks for verified, production-quality, publication-quality, or physics-sensitive Wolfram code;
- the answer uses unfamiliar package APIs or version-sensitive packages;
- generated code could be expensive, destructive, or misleading if wrong;
- the user asks whether an answer hallucinated Wolfram symbols.

Strict validation requires:

1. A package or resource evidence card.
2. A named prompt/example candidate when relevant.
3. A load, syntax, static, or smoke test.
4. A mathematical or physical sanity check for scientific workflows.
5. A remaining-uncertainty note when anything could not be verified.

## Evidence card

Use this compact structure when resource-aware or strict mode applies:

```markdown
### Wolfram evidence

- Package or resource:
- Source checked:
- Load command:
- Symbols used:
- Minimal example:
- Adaptation map:
- Smoke test:
- Conventions:
- Remaining uncertainty:
```

The evidence card is not a license to paste long documentation. Summarize the pattern and cite or name the resource.

## Fail closed

Fail closed whenever verification is missing.

- Do not invent prompt names, example names, package contexts, option names, or symbols.
- Do not claim a Wolfram resource was consulted unless it was actually available in the current environment.
- If live lookup is unavailable, switch to Docs-only mode and say so.
- If a package example cannot be run, provide static checks and mark runtime validation as not performed.
- If sources disagree, prefer the version matching the installed package or the user's environment.

## Credentials and security

No secrets belong in this repository.

- Use environment variables, OS keychain storage, Wolfram secure credential mechanisms, or the user's existing local configuration.
- Never commit API keys, secured authentication keys, cookies, Wolfram account data, notebook outputs containing secrets, or private project snippets.
- Ask before indexing private notebooks, proprietary package docs, or unpublished research code.
- Treat generated Wolfram code as untrusted until reviewed. Do not run destructive code without user approval.

## Cache policy

Cache only public metadata or user-approved snippets.

Suggested local paths:

- `data/wolfram-resource-manifest.json` for curated prompt/example metadata.
- `artifacts/verified-example-snippets.jsonl` for optional public snippets gathered by future tooling.
- `artifacts/semantic-index/` for optional future semantic search artifacts.

Cache entries should include source names, retrieval time, and enough context to reproduce the lookup. They should not include credentials or private source material unless the user explicitly asks for that behavior.

## Manifest use

Read `data/wolfram-resource-manifest.json` as the local inventory of candidate resources and validation fields. Treat it as a routing aid:

1. Match the user's request to a mode.
2. Select likely prompt/example candidates from the manifest.
3. Verify availability through local docs, installed Wolfram tooling, or live Wolfram access when allowed.
4. Build the evidence card.
5. Generate the answer and include checks.

The manifest is intentionally conservative. If a resource cannot be verified, do not use it as evidence.

## Offline lookup helper

Use `scripts/wolfram_resource_lookup.py` to rank manifest entries without network access:

```bash
python scripts/wolfram_resource_lookup.py --kind prompts --query "add comments to this Mathematica code"
python scripts/wolfram_resource_lookup.py --kind examples --query "rerank semantic search snippets"
```

The helper only searches the local manifest. Its output is a candidate list, not proof that a live Wolfram prompt or example was consulted.

## Example extraction helper

Use `scripts/extract_wl_examples.py` to collect local examples into JSONL before building future evidence caches:

```bash
python scripts/extract_wl_examples.py README.md Documentation/ Examples/ --output artifacts/verified-example-snippets.jsonl
```

The extractor supports fenced Markdown blocks labeled `Mathematica`, `Wolfram`, `WolframLanguage`, `wl`, or `mma`, plus whole `.wl` and `.m` files. It does not parse `.nb` notebooks; convert or export notebook examples before extraction.
