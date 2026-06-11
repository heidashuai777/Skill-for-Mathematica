# Wolfram Language Style Guide for Human-Readable Mathematica Code

## Structure

Organize code in this order:

1. Setup and package loading.
2. Assumptions and constants.
3. Definitions.
4. Derivation or computation.
5. Visualization or output.
6. Checks.

Use comments to explain intent and physics, not obvious syntax.

```Mathematica
(* Define assumptions once and reuse them. *)
assumptions = {mass > 0, frequency > 0, hbar > 0};

(* Harmonic oscillator ground-state wavefunction. *)
psi0[x_] := (mass frequency/(Pi hbar))^(1/4) Exp[-mass frequency x^2/(2 hbar)];

normalizationCheck =
  FullSimplify[
    Integrate[Conjugate[psi0[x]] psi0[x], {x, -Infinity, Infinity}],
    assumptions
  ];
```

## Naming

Use names that communicate meaning. Conventional physics symbols are fine when they are standard.

Good examples:

```Mathematica
radialEquation
potentialEnergy
metricComponents
wavefunction
hbar
omega
psi
rho
```

Avoid using `Subscript` as a computational variable. It is good for display but fragile in code.

## Scoping

Use `Module` for local variables in reusable functions.

```Mathematica
ClearAll[effectivePotential]
effectivePotential[angularMomentum_, mass_, radius_] := Module[
  {centrifugalTerm, gravitationalTerm},
  centrifugalTerm = angularMomentum (angularMomentum + 1)/radius^2;
  gravitationalTerm = -2 mass/radius;
  centrifugalTerm + gravitationalTerm
]
```

## Symbolic and Numerical Work

Keep symbolic derivation separate from numerical evaluation.

```Mathematica
symbolicResult = FullSimplify[expr, assumptions];

numericParameters = {mass -> 1, frequency -> 2, hbar -> 1};
numericResult = N[symbolicResult /. numericParameters, 30];
```

## Assumptions

Use explicit assumptions. Prefer:

```Mathematica
FullSimplify[expr, assumptions]
```

over hidden notebook state.

## Functions to Prefer

- `NDSolveValue` when the desired result is an interpolating function.
- `DSolveValue` when the desired result is the expression itself.
- `Association` for structured parameters.
- `Dataset` for tabular inspection.
- `Quantity` only when units are central and supported by the computation.

## Plotting

Make plots self-explanatory.

```Mathematica
Plot[
  Evaluate[potentialEnergy[x]],
  {x, xmin, xmax},
  AxesLabel -> {"x", "V(x)"},
  PlotLabel -> "Potential energy",
  PlotRange -> All
]
```

## Comments

Useful comments:

```Mathematica
(* The boundary condition enforces regularity at r = 0. *)
(* The next line follows the documented tensor-package pattern: define manifold before metric. *)
```

Less useful comments:

```Mathematica
(* Set x equal to 1. *)
x = 1;
```

## Reproducibility

- Set random seeds with `SeedRandom`.
- Record package versions if available.
- Keep parameter values in one place.
- Avoid relying on notebook state.
- Include a final check cell or test block.
