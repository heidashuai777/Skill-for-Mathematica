---
name: mathematica-codex-helper
description: Use when writing, reviewing, debugging, or explaining Wolfram Language / Mathematica code, notebooks, paclets, or math/physics derivations. This skill emphasizes human-readable code and package accuracy by grounding every nontrivial package call in manuals, examples, and smoke tests, especially for physics packages such as xAct, FeynCalc, FeynArts, FeynRules, Package-X, MaTeX, Q3, QuESTlink, Black Hole Perturbation Toolkit packages, and other domain paclets.
metadata:
  short-description: Human-readable Mathematica with manual-backed package usage.
---

# Mathematica Codex Helper

## Purpose

Produce Mathematica / Wolfram Language code that a human physicist can read, modify, and trust. When a solution depends on a package, especially a physics package, first ground the implementation in the package manual and its examples. Treat examples as executable specifications: learn the loading syntax, argument order, naming conventions, options, and expected output from them before adapting the code.

## Hard Rules

1. Do not invent package APIs. For every unfamiliar package symbol, consult local references, official documentation, paclet pages, example notebooks, tutorials, tests, or source examples before using it.
2. Prefer built-in Wolfram Language functions when they solve the problem clearly. Use external packages only when they add necessary domain functionality.
3. If documentation or examples are unavailable, say which function or convention is uncertain and provide either a built-in fallback or a minimal reproducible question for the user.
4. For physics work, state conventions before code: units, metric signature, coordinate order, index positions, Fourier transform convention, normalization, and assumptions.
5. Keep code readable. Avoid dense one-liners unless the user explicitly asks for compact code.
6. Validate code through syntax checks, package-load checks, unchanged manual examples, adapted smoke tests, and physical sanity checks whenever possible.

## Package Manual + Example Workflow

When a package is involved, use this loop:

1. **Locate evidence**
   - Search the repository, local docs, package examples, tutorial notebooks, test files, or official manual pages.
   - Prefer official package docs and examples over blog posts or memory.
   - For a package already in the repo, inspect its `README`, `Documentation`, `Examples`, `Tests`, `.wl`, `.m`, and `.nb` files.

2. **Build a mini package card**
   - Package name and context.
   - Correct loading command, usually `Needs["context`"]` or the package's documented loader.
   - Symbols to use.
   - Minimal manual example.
   - Options and assumptions that matter.
   - Known pitfalls or version-sensitive syntax.

3. **Run examples before adaptation**
   - Load the package.
   - Run the smallest official example unchanged when possible.
   - Only then replace symbols, variables, dimensions, fields, manifolds, or parameters for the user's problem.

4. **Adapt incrementally**
   - Change one thing at a time from the official example.
   - Keep a mapping such as `manualExampleVariable -> userProblemVariable`.
   - Preserve the package's required order of definitions. For example, tensor packages often require defining manifolds and metrics before tensors or covariant derivatives.

5. **Record evidence in the answer**
   - Briefly state which manual/example pattern the code follows.
   - Do not paste large copyrighted manual passages. Summarize usage patterns and include only short snippets when necessary.

For a fuller procedure, read `references/manual-example-integration.md`.

## Mathematica Style Rules

Follow `references/wolfram-style-guide.md`. Core rules:

- Start scripts with `ClearAll["Global`*"]` only when appropriate for a standalone notebook or script.
- Use descriptive names: `radialCoordinate`, `timeGrid`, `hamiltonian`, `metricTensor`.
- Avoid `Subscript[x, 1]` as a program variable. Use `x1`, `x[1]`, or associations.
- Separate symbolic and numerical stages.
- Put assumptions in one place, e.g. `assumptions = {m > 0, omega > 0, hbar > 0};`.
- Use `Simplify[expr, assumptions]` or `FullSimplify[expr, assumptions]` rather than relying on global state.
- Prefer `NDSolveValue` over `NDSolve` when the desired result is an interpolating function.
- Use `Module` for local scope in reusable functions.
- Use comments to explain physics and package-specific steps, not obvious syntax.
- Keep plots reproducible with explicit ranges, legends, labels, and units.

## Physics Package Accuracy Rules

Follow `references/physics-package-playbook.md`. Always check:

- Conventions: units, metric signature, coordinates, index order, normalization, Fourier sign.
- Dimensions: scalar, vector, matrix, tensor rank, spinor dimension, Hilbert-space dimension.
- Symmetry: Hermiticity, tensor symmetries, gauge constraints, conservation laws.
- Limits: zero-coupling, flat-space, nonrelativistic, classical, small-parameter, or known analytic limits.
- Numerical stability: precision, stiffness, domain boundaries, singular points.

## Response Template

For nontrivial tasks, structure the answer as:

1. **Plan and conventions**
2. **Derivation**
3. **Manual/example evidence**
4. **Mathematica code**
5. **Checks and interpretation**

Use this code block language tag:

```Mathematica
(* Mathematica / Wolfram Language code here *)
```

## Validation Checklist

Before finalizing code, run as many of these as possible:

```Mathematica
$Version
Needs["PackageContext`"]
Names["PackageContext`*"]
Information[symbol]
Options[symbol]
```

For a standalone `.wl` file, use:

```bash
wolframscript -script path/to/file.wl
```

If `wolframscript` is unavailable, do static checks and clearly say that runtime validation was not performed. Helper scripts are provided in `scripts/`.

## Example Triggers

- "Write readable Mathematica code for the hydrogen radial equation and verify normalization."
- "Use xAct to compute Christoffel symbols and Ricci scalar for this metric."
- "Use FeynCalc for a gamma-matrix trace, but follow the official examples."
- "Convert this physics derivation into a well-commented Mathematica notebook."
- "Debug this Mathematica package code and check whether the package API is being used correctly."
