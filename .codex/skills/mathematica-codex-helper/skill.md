---
name: mathematica-codex-helper
description: Use this skill whenever writing, reviewing, debugging, or explaining Wolfram Language / Mathematica code, notebooks, paclets, or math/physics derivations. It enforces human‑readable code, explicit physics conventions, and accurate package usage by grounding nontrivial calls in manuals, examples, and smoke tests – especially for physics packages such as xAct, FeynCalc, FeynArts, FeynRules, Package‑X, MaTeX, Q3, QuESTlink, black‑hole paclets, and more.
metadata:
  short-description: Human‑readable Mathematica with manual‑backed package usage and physics‑aware guardrails.
---

# Mathematica Codex Helper

## Purpose

This skill gives Codex domain expertise in writing and explaining Mathematica code for mathematical and physics workflows. It aims to:

- Produce code that a physicist can read, modify, and trust.
- Provide full mathematical derivations and physical context alongside the code.
- Avoid hallucinating package APIs by consulting official manuals, examples, paclet docs, test suites, and source when needed.
- Clarify physics conventions (units, metric signatures, coordinate order, index positions, normalization, Fourier convention, etc.) before deriving or computing anything.
- Include physical and mathematical sanity checks to catch bugs early.
- Separate symbolic derivations from numerical evaluations and keep code reproducible.

## Hard Rules

1. **Ground package usage in evidence**. Never invent APIs or guess symbol contexts. For every unfamiliar symbol or package call, consult official documentation, paclet pages, tutorial notebooks, tests, or source examples. Prefer manual examples over blog posts or memory. If you cannot find evidence, state the uncertainty and provide a built‑in fallback or ask the user for more context.

2. **Prefer built‑in functionality**. Use built‑in Wolfram Language functions whenever they solve the problem clearly. Load external packages only when necessary for domain‑specific features.

3. **Declare conventions explicitly**. Before writing code, state the unit system (SI, natural units, geometrized, etc.), metric signature (mostly plus vs. mostly minus), coordinate order, index variance (covariant vs. contravariant), Fourier transform convention, normalization of states, and boundary conditions. This prevents mismatches when using tensor and quantum packages.

4. **Keep the code readable**. Avoid dense one‑liners unless explicitly requested. Use descriptive variable names, indent logically, and separate code blocks with blank lines. Put assumptions and parameters in one place and reuse them.

5. **Validate everything**. Run syntax checks (`Information[symbol]`, `Options[symbol]`), load checks (`Needs["Context``"]`), and small smoke tests before adapting package examples. For physics code, always include at least one physical or mathematical check (e.g., normalization, Hermiticity, symmetry properties, known limits) to confirm the result.

## Package Manual + Example Workflow

When a package is involved, follow this workflow:

1. **Locate evidence**. Search in order: official paclet docs (Mathematica doc center), included tutorial notebooks and examples, test files, source code, repository README, maintainer blog posts, and, as a last resort, general web examples. Document the sources used.

2. **Build a package evidence card**. Summarize: package name, version, loading command (`Needs["Context``"]` or documented loader), symbols to use, a minimal official example, important options, assumptions, and any pitfalls or version differences.

3. **Run a minimal example unchanged**. Load the package and run the smallest official example that uses the required symbol. Verify that the example runs without errors and returns the documented result.

4. **Adapt incrementally**. Change variables, dimensions, or options one at a time. Maintain a mapping from the manual example variables to the user’s problem. Respect the order of definitions (e.g., define manifolds and metrics before tensors). Test after each change.

5. **Record evidence in the answer**. Briefly state which manual example pattern the code follows. Do not copy large chunks of manual text; instead, summarise usage patterns and mention any key options or caveats. When uncertain, explicitly note the uncertainty.

## Mathematica Style Guidelines

Use a clear structure:

1. **Setup & packages**. Load built‑in packages with `Needs["Context``"]`, and clear the global context if appropriate (`ClearAll["Global`*"]`).
2. **Assumptions & constants**. Collect all physical constants and assumptions into `assumptions = {...}` and reuse them with `FullSimplify` or `Integrate`.
3. **Definitions**. Define functions and variables with descriptive names. Use `Module` for local scope.
4. **Derivation / computation**. Perform symbolic derivations first, then substitute numerical values only if needed. Use `Simplify`, `FullSimplify`, `Assuming`, etc. Avoid mixing symbolic and numerical evaluations.
5. **Visualization / output**. Plot results with labels and ranges. Use `PlotLabel`, `AxesLabel`, and units where appropriate.
6. **Checks & validation**. Include tests such as normalization integrals, Hermiticity tests, flat‑space or classical limits, or dimension checks.

Naming conventions:

- Use descriptive names like `radialCoordinate`, `metricTensor`, `hamiltonian`, `effectivePotential`, etc.
- Use standard physics symbols (`ψ`, `hbar`, `ω`) only for well‑known quantities; avoid cryptic short names otherwise.
- Avoid using `Subscript[x,1]` as a variable; use `x1` or `x[1]` for computational purposes.

Separate symbolic and numerical code:

```Mathematica
(* Symbolic derivation *)
symbolicResult = FullSimplify[expr, assumptions];

(* Numerical evaluation *)
numericParams = {m -> 1, ω -> 2, ℏ -> 1};
numericResult = N[symbolicResult /. numericParams, 30];
```

Use explicit assumptions instead of hidden global assumptions:

```Mathematica
FullSimplify[expr, assumptions]
```

Plotting best practices:

```Mathematica
Plot[
  Evaluate[potential[x]],
  {x, xmin, xmax},
  AxesLabel -> {"x", "V(x)"},
  PlotLabel -> "Potential Energy",
  PlotRange -> All
]
```

## Physics Package Accuracy Rules

For domain packages (xAct, FeynCalc, FeynRules, Package‑X, Q3, QuESTlink, BHPT paclets, etc.), always check:

- **Conventions**: units, metric signature, coordinate order, index variance, gamma matrix conventions, Dirac sign convention, Fourier transform sign, spinor basis, state normalization. Many packages have built‑in choices (e.g., xAct uses mostly minus). Document them.

- **Dimensions**: confirm scalar vs. vector vs. matrix vs. tensor rank, Hilbert space dimension, spinor dimension. Many packages require specifying dimensionality explicitly.

- **Symmetries & identities**: check whether tensors are symmetric, antisymmetric, hermitian, etc. Use `TensorSymmetry` or package‑specific canonicalization. Verify gauge invariants, conservation laws, or conserved quantities.

- **Limits & checks**: test zero‑coupling limits, flat‑space limits, low‑multipole or high‑energy limits, classical limits (`ℏ → 0`), etc. If the package is used for GR, check the Schwarzschild limit of Kerr; if for QFT, check trace identities; if for QM, verify normalization and Hermiticity.

- **Version differences**: document any version‑specific syntax or options. Many physics paclets change APIs across releases; always check the documentation for the installed version.

## Response Template

When using this skill for a nontrivial task, structure the answer as follows:

1. **Plan & conventions**. Briefly explain the problem, identify required packages, and state conventions (units, signature, etc.).
2. **Mathematical derivation**. Present step‑by‑step derivations, including equations used and assumptions. Use Wolfram Language functions for symbolic checks when appropriate.
3. **Manual/example evidence**. Summarize which manual examples you consulted, what they taught you (e.g., the correct loading command and argument order), and how you adapted them.
4. **Mathematica code**. Provide the complete code in a fenced `Mathematica` code block. Include comments to map the code to the derivation and note any package conventions.
5. **Checks & interpretation**. Show at least one numerical or symbolic check of the result. Interpret the output in context.

Use fenced code blocks like this:

```Mathematica
(* Mathematica / Wolfram Language code *)
```

## Example Triggers

Trigger this skill when the user asks to:

- “Write a readable Mathematica script for the hydrogen atom radial equation and verify normalization.”
- “Solve the Schrödinger equation for a harmonic oscillator using the Quantum paclet; include derivation.”
- “Use xAct to compute Christoffel symbols and the Ricci scalar of this metric, following the official examples.”
- “Use FeynCalc for a gamma matrix trace; follow the manual examples and show smoke tests.”
- “Convert this physics derivation into a Mathematica notebook‑style script.”
- “Debug this Mathematica package code and check whether the package API is used correctly.”

## Further Reading

This skill comes with additional references located in the `references/` directory:

- `manual-example-integration.md` – A detailed protocol for integrating official package manuals and examples into your workflow. It includes source prioritisation, how to build an evidence card, extraction methods, adaptation guidelines, validation layers, and anti‑hallucination rules.
- `wolfram-style-guide.md` – A style guide for human‑readable Mathematica code, covering structure, naming, scoping, symbolic vs. numerical work, plotting, comments, and reproducibility.
- `physics-package-playbook.md` – A playbook of guardrails for physics packages, including guidelines and checks for xAct, FeynCalc, FeynRules, Package‑X, quantum paclets, black‑hole perturbation paclets, and more.

Refer to these documents for deeper examples and best practices.