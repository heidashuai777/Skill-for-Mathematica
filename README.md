# Skill for Mathematica

This repository contains a Codex skill for writing readable Mathematica / Wolfram Language code with stronger package accuracy, especially for physics packages.

The skill is located at:

```text
.codex/skills/mathematica-codex-helper/SKILL.md
```

A lowercase copy is also included at:

```text
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

```text
.codex/skills/mathematica-codex-helper/references/manual-example-integration.md
.codex/skills/mathematica-codex-helper/references/wolfram-style-guide.md
.codex/skills/mathematica-codex-helper/references/physics-package-playbook.md
```

## Typical requests

```text
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
