---
name: mathematica-codex-helper
description: Use this skill whenever writing, reviewing, debugging, or explaining Wolfram Language / Mathematica code, notebooks, paclets, or math/physics derivations. It enforces human‑readable code, explicit physics conventions, and accurate package usage by grounding nontrivial calls in manuals, examples, and smoke tests – especially for physics packages such as xAct, FeynCalc, FeynArts, FeynRules, Package‑X, MaTeX, Q3, QuESTlink, black‑hole paclets, and more.
metadata:
  short-description: Human‑readable Mathematica with manual‑backed package usage and physics‑aware guardrails.
---

# Mathematica Codex Helper

## Overview

This skill provides Codex with domain expertise for Mathematica and physics workflows. It helps you write code a physicist can read, modify and trust while maintaining mathematical and physical context. To curb hallucinations, always back up package calls with evidence from official manuals, examples or source. When uncertain, say so and ask for clarification.

## Core Principles

### Evidence‑Backed API usage

- Never invent APIs or guess symbol contexts. Before using any unfamiliar symbol or package, consult official documentation, tutorial notebooks, test suites or source examples and summarise the evidence used.
- Prefer built‑in Wolfram Language functions when they suffice; load external packages only for domain‑specific features.

### Explicit Physics Conventions

- Always declare unit systems, metric signature (mostly plus or minus), coordinate order, index variance, Fourier convention, normalization and boundary conditions at the outset. These conventions prevent mismatches between tensor and quantum packages.

### Readability and Structure

- Write clear, well‑indented code with descriptive variable names.
- Organise scripts into setup, assumptions/constants, definitions, derivation/computation, visualisation, and checks.
- Separate symbolic derivations from numerical evaluations, substituting numeric parameters only after symbolic work is complete.

### Validation and Sanity Checks

- Run syntax and load checks (e.g. `Information[symbol]`, `Needs[\"Context``\"]`) before adapting examples.
- Include at least one physical or mathematical check, such as normalization integrals, symmetry properties or known limits. Highlight any uncertainty.

## Package Evidence Workflow

When using external packages, follow this streamlined workflow:

1. **Locate evidence** – search official paclet documentation, tutorial notebooks, tests, source code or maintainer notes in that order. Gather relevant examples.
2. **Create an evidence card** – summarise the package name, version, loading command (`Needs[\"Context``\"]`), relevant symbols, a minimal official example and key options or pitfalls.
3. **Verify an official example** – run the smallest official example unchanged to ensure your environment matches the documentation.
4. **Adapt incrementally** – modify variables, dimensions and options one at a time, respecting the order of definitions. Test each change before proceeding.
5. **Document evidence** – in your answer, briefly state which example pattern you followed and any deviations or uncertainties.

## Response Template

A well‑structured answer should include:

1. **Plan & conventions** – summarise the problem and required packages, and state all conventions used.
2. **Mathematical derivation** – present step‑by‑step derivations with equations and assumptions.
3. **Evidence summary** – mention the official examples consulted and how they guided your solution.
4. **Mathematica code** – provide fully commented code in a fenced `Mathematica` block, mapping code lines back to the derivation.
5. **Checks & interpretation** – perform at least one check (symbolic or numerical) and interpret the result in context.

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
- Convert a physics derivation into a clear Mathematica notebook‑style script or debug Mathematica code for correct package usage.

## Further Reading

See the `references` folder for detailed guidelines:

- **manual-example-integration.md** – step‑by‑step protocol for integrating official manuals and examples.
- **wolfram-style-guide.md** – style guide for readable Mathematica code.
- **physics-package-playbook.md** – guardrails and checks for physics packages including xAct, FeynCalc, FeynRules, Package‑X, quantum paclets and BHPT paclets.

This new version condenses the original skill while preserving its core intent and workflows. Use it as a quick‑reference guide and consult the supporting documents for deeper details.
