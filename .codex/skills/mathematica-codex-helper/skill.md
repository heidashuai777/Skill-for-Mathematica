---
name: mathematica-codex-helper
description: Use when writing, reviewing, debugging, or explaining Wolfram Language / Mathematica code, notebooks, paclets, package docs, or math/physics derivations, especially when correctness depends on manuals, Wolfram Prompt Repository assets, Wolfram Example Repository patterns, smoke tests, explicit conventions, or physics packages such as xAct, FeynCalc, FeynArts, FeynRules, Package-X, MaTeX, Q3, QuESTlink, and black-hole paclets.
---

# Mathematica Codex Helper

## Overview

This skill helps Codex write Wolfram Language code that a mathematician or physicist can read, modify, and trust. Ground nontrivial package usage in official manuals, examples, installed docs, source, or verified Wolfram resources before generating code. When evidence is unavailable, say so and narrow the answer.

## Core Principles

### Evidence-backed API usage

- Never invent APIs, option names, package contexts, or symbol meanings. Before using any unfamiliar symbol or package, consult official documentation, tutorial notebooks, test suites, source examples, or verified Wolfram resources and summarize the evidence used.
- Prefer built‑in Wolfram Language functions when they suffice; load external packages only for domain‑specific features.

### Explicit Physics Conventions

- Declare unit systems, metric signature, coordinate order, index variance, Fourier convention, normalization, and boundary conditions before doing physics work.
- Keep conventions visible when moving between tensor, quantum, QFT, numerical, and visualization code.

### Readability and Structure

- Write clear, well-indented code with descriptive variable names.
- Organize scripts into setup, assumptions/constants, definitions, derivation/computation, visualization, and checks.
- Separate symbolic derivations from numerical evaluations, substituting numeric parameters only after symbolic work is complete.

### Validation and Sanity Checks

- Run syntax and load checks (e.g. `Information[symbol]`, `Needs["Context``"]`) before adapting examples.
- Include at least one physical or mathematical check, such as normalization integrals, symmetry properties, conservation laws, or known limits.
- Highlight uncertainty and state when runtime execution was not possible.

## Wolfram resource routing

Use Wolfram resource routing when the task needs a canonical usage pattern, code transformation, package documentation, naming suggestions, or an assessment pass.

Prefer these candidate Wolfram Prompt Repository assets when they match the request:

| Request type | Candidate prompt |
| --- | --- |
| Short canonical sample code | `WolframSampleCode` |
| Reformat or clean code | `CodeReformat` |
| Add comments | `CodeCommentInsert` |
| Draft package docs or `::usage` text | `CodeDocAnnotator` |
| Improve function names | `FunctionNameSuggest` |
| Improve variable names | `VariableNameSuggest` |
| Assess hallucination risk or answer quality | `LLMPromptAssessment` |

Use Wolfram Example Repository patterns for retrieval architecture, tool-mediated evidence lookup, and reranking workflows. Candidate examples are tracked in `data/wolfram-resource-manifest.json`.

Fail closed: do not claim that a prompt, example notebook, or live Wolfram lookup was used unless it was actually verified in the current environment. If live resources are unavailable, continue in docs-only mode and say so.

## Resource-aware workflow

For nontrivial package, physics, documentation, or code-transformation tasks:

1. Classify the task as docs-only, resource-aware, or strict validation mode.
2. Read `references/wolfram-resource-integration.md` when named Wolfram prompts/examples, credentials, cache policy, or strict validation apply.
3. Use `data/wolfram-resource-manifest.json` as the local inventory of candidate prompt/example names and required evidence fields.
4. Use `scripts/wolfram_resource_lookup.py` for offline manifest ranking when a query maps to multiple resources.
5. Build a compact evidence card before generating package-dependent code.
6. Generate the answer from verified patterns, adapting one concept at a time.
7. Include a smoke test and one mathematical or physical sanity check when relevant.

### Wolfram evidence card

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

## Package Evidence Workflow

When using external packages, follow this streamlined workflow:

1. **Locate evidence** - search official paclet documentation, tutorial notebooks, tests, source code, verified Wolfram resources, or maintainer notes in that order.
2. **Create an evidence card** - summarize the package name, version/source, loading command, relevant symbols, minimal example, key options, conventions, and uncertainty.
3. **Verify an official example** - run the smallest official example unchanged when possible.
4. **Adapt incrementally** - modify variables, dimensions, conventions, and options one at a time, respecting documented setup order.
5. **Document evidence** - briefly state which example pattern or resource guided the answer and where verification stopped.

## Response Template

A well-structured answer should include:

1. **Plan and conventions** - summarize the problem and required packages, and state all conventions used.
2. **Mathematical derivation** - present step-by-step derivations with equations and assumptions.
3. **Evidence summary** - mention official docs, examples, or Wolfram resources consulted and how they guided the solution.
4. **Mathematica code** - provide readable code in a fenced `Mathematica` block, mapping code lines back to the derivation when helpful.
5. **Checks and interpretation** - perform at least one check and interpret the result in context.

Use fenced code blocks like:

```Mathematica
(* Mathematica / Wolfram Language code *)
```

## Trigger Examples

Invoke this skill when a user asks to:

- Write a readable Mathematica script for the hydrogen atom radial equation and verify normalization.
- Solve the Schrödinger equation for a harmonic oscillator using the Quantum paclet, including derivation.
- Compute Christoffel symbols and Ricci scalars with xAct following official examples.
- Perform gamma matrix traces with FeynCalc, citing the manual examples and running smoke tests.
- Convert a physics derivation into a clear Mathematica notebook-style script or debug Mathematica code for correct package usage.
- Reformat, comment, document, or rename Wolfram Language code using resource-aware prompt routing.
- Check whether a Wolfram Language answer hallucinated package symbols, contexts, options, or conventions.

## Further Reading

See the `references` folder for detailed guidelines:

- **wolfram-resource-integration.md** - resource-aware modes, Wolfram Prompt Repository routing, Wolfram Example Repository patterns, credentials, cache policy, and strict validation.
- **manual-example-integration.md** - step-by-step protocol for integrating official manuals and examples.
- **wolfram-style-guide.md** - style guide for readable Mathematica code.
- **physics-package-playbook.md** - guardrails and checks for physics packages including xAct, FeynCalc, FeynRules, Package-X, quantum paclets, and BHPT paclets.

Use this file as a quick-reference guide. Load the supporting documents only when their details are needed.
