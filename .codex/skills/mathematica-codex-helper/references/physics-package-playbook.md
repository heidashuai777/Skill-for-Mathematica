# Physics Package Playbook

This file gives package-aware guardrails for Mathematica code in physics. It is intentionally conservative: verify package syntax from manuals and examples before use.

## Universal Physics Conventions

Before writing code, record these choices:

- Unit system: SI, natural units, geometrized units, or custom.
- Metric signature: mostly plus or mostly minus.
- Coordinate order.
- Index convention: covariant, contravariant, frame, coordinate, spinor.
- Fourier transform convention.
- State normalization.
- Boundary conditions.
- Domain assumptions.

## Built-in First

Use built-in Wolfram Language tools when they are enough:

- `DSolveValue`, `NDSolveValue`, `DEigensystem`.
- `Eigensystem`, `MatrixExp`, `KroneckerProduct`.
- `TensorReduce`, `TensorContract`, `TensorProduct`.
- `CoordinateChartData`, `TransformedField`.
- `Quantity` and `UnitConvert` when physical units matter.

Use external physics packages when built-ins are cumbersome or domain-specific syntax is needed.

## xAct Family

Typical use cases: differential geometry, tensor algebra, perturbation theory, abstract index notation.

Manual-backed steps usually look like:

1. Load the documented xAct subpackage.
2. Define manifold and indices.
3. Define metric and covariant derivative.
4. Define tensors and symmetries.
5. Compute curvature, contractions, or perturbations.
6. Simplify using package-specific canonicalization functions.

Accuracy checks:

- Confirm index variance and coordinate order.
- Check metric signature.
- Test flat-space or known metric limits.
- Verify expected tensor symmetries.

## FeynCalc and Related QFT Packages

Typical use cases: gamma algebra, Lorentz contractions, amplitudes, loop-integral manipulation.

Manual-backed steps usually look like:

1. Load the documented package context.
2. Use package-native representations for momenta, scalar products, gamma matrices, and propagators.
3. Convert expressions into the package's internal form if the manual requires it.
4. Apply simplification and contraction functions in the documented order.
5. Convert output back to standard display form if needed.

Accuracy checks:

- Confirm metric and gamma-matrix conventions.
- Verify dimensions for dimensional regularization.
- Test simple traces or scalar products against known results.
- Avoid mixing notations from different QFT packages without explicit conversion.

## FeynArts, FeynRules, Package-X, SARAH, FormTracer

These packages are version-sensitive. Always inspect their examples before use.

Common pitfalls:

- Model files must be loaded in the documented order.
- Symbol names may belong to package contexts.
- Options differ across versions.
- Generated expressions may need conversion before being passed to another package.

Record the source example that controls the workflow.

## Quantum Packages

Examples: Q3, QuESTlink, and other quantum-information packages.

Check:

- Basis ordering.
- Tensor-product convention.
- Whether states are kets, vectors, density matrices, or symbolic objects.
- Normalization.
- Hermiticity and trace preservation.
- Gate ordering and measurement convention.

Smoke tests:

```Mathematica
Chop[Tr[densityMatrix] - 1]
Chop[hamiltonian - ConjugateTranspose[hamiltonian]]
```

## General Relativity and Black-Hole Packages

Examples: Black Hole Perturbation Toolkit packages and related paclets.

Check:

- Coordinate system.
- Mass and spin parameter definitions.
- Tortoise coordinate convention.
- Harmonic index conventions.
- Boundary condition names.
- Whether quantities are symbolic, numerical, or interpolating functions.

Use known limits:

- Schwarzschild limit from Kerr.
- Flat-space or large-radius asymptotics.
- Low multipole behavior when applicable.

## Final Answer Requirements for Physics Code

A good final answer includes:

1. Conventions.
2. Mathematical derivation.
3. Package evidence.
4. Readable Mathematica code.
5. At least one mathematical or physical check.

If runtime execution was not possible, say so explicitly and still provide static and conceptual checks.
