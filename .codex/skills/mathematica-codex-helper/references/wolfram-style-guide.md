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

## Sectioning Template

Every nontrivial `.wl` program should be readable without running it. Divide it into sections and, when a section has multiple responsibilities, subsections:

```Mathematica
(* ::Section:: *)
(* Setup *)

ClearAll["Global`*"];
$HistoryLength = 0;
SetDirectory["/home/Heidashuai/claude/higgs_bbgamma"];

(* ::Section:: *)
(* Conventions and Inputs *)

(* Kinematic rules are centralized so the main calculation never hides a convention. *)
kinematicRules = {...};
inputFiles = <|...|>;

(* ::Section:: *)
(* Helper Definitions *)

ClearAll[quietLog, safeSimplify];

(* ::Section:: *)
(* Main Calculation *)

(* This section creates physics results. It should not contain audit-only code. *)
mainResult = ...;

(* ::Section:: *)
(* Output *)

Put[mainResult, "stage_outputs/main_result.m"];

(* ::Section:: *)
(* Verification *)

verificationReport = <|...|>;
Put[verificationReport, "stage_outputs/checks.m"];
```

Use `(* ::Subsection:: *)` for setup blocks such as package loading, paths, assumptions, and reusable helpers. Keep the main calculation and verification separate; do not bury checks inside the calculation loop unless they are required to prevent invalid intermediate data.

## Concision and Repetition

Prefer the shortest clear Wolfram Language form:

```Mathematica
SetDirectory["/home/Heidashuai/claude/higgs_bbgamma"];
```

instead of:

```Mathematica
projectDir = "/home/Heidashuai/claude/higgs_bbgamma";
SetDirectory[projectDir];
```

Introduce a named variable only when it is reused, clarifies a convention, or will be written to a summary. After a script works, reread it and remove one-use wrappers, redundant `writeWL` variants, stale debugging probes, and repeated path joins that can be replaced by one association.

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

## Quiet Logging and Diagnostics

Avoid raw `Print` in reusable scripts because it makes long calculations noisy and hard to resume. Prefer returned associations, status files, `Echo` for short interactive probes, and `Message` for package-style diagnostics.

```Mathematica
ClearAll[quietLog, writeStatus];

quietLog[message_String, verbose_: False] :=
  If[TrueQ[verbose], Echo[message, "status"]];

writeStatus[path_String, status_Association] :=
  Put[Append[status, "Timestamp" -> DateString[{"ISODate", " ", "Time"}]], path];
```

Use `Print` only for command-line scripts where the user explicitly needs live progress and keep it short. For long jobs, write `status.m`, `summary.m`, or CSV diagnostics instead.

## Package Conflict Safety

Official Wolfram package workflows use contexts and package loading functions such as `Needs` and `BeginPackage`. Keep package interactions isolated:

- Put all `Needs`/`Get` calls in setup.
- Load packages in a deterministic order.
- After loading packages with overlapping symbol names, check `Context /@ Names["symbolName"]` or call package functions with explicit contexts.
- Wrap noisy third-party package initialization in `Block[{$Output = {}}, ...]` only when the banner is unimportant and the load result is verified.
- Do not leave package-private heads, debug wrappers, or context-specific placeholders in final outputs.
- When a package may conflict with another one, make a minimal smoke test before using it in the main calculation.

## Main Calculation vs Verification

Keep production results and checks separate:

- The main calculation section produces the primary expressions, rules, integrals, plots, or datasets.
- The verification section checks dimensions, limits, substitutions, forbidden symbols, package heads, numeric spot checks, and file existence.
- Verification may fail without corrupting the main output; write checks to a separate report.
- Store enough metadata in summaries for reruns: Wolfram version, package versions if available, assumptions, input files, output files, and memory-sensitive options.

## Efficiency Rules

Use built-in structure before expensive symbolic operations:

- Use `Dispatch[rules]` for large replacement rule sets.
- Use `Together`, `Cancel`, `Factor`, or `Collect` before global `FullSimplify`.
- Use `FullSimplify[expr, assumptions, TimeConstraint -> seconds]` or `TimeConstrained[...]` for large expressions.
- Prefer `Map`, `MapThread`, `AssociationMap`, and `KeyValueMap` over repeated indexing loops when this improves clarity.
- Use `ParallelMap` or `ParallelTable` for independent, side-effect-free tasks only. Distribute definitions explicitly when kernels need local helper functions or package contexts, and avoid parallel writes to the same file.
- Choose parallel granularity intentionally. Many small uneven tasks benefit from finer grain; large similar tasks benefit from coarser grain to reduce overhead.
- Monitor memory before launching parallel symbolic jobs. More kernels can be slower if every kernel copies large expressions.

## Result Simplification Loop

Continuously simplify output results, but keep simplification auditable:

```Mathematica
ClearAll[safeSimplify, bestByLeafCount];

safeSimplify[expr_, assumptions_, seconds_: 30] := Module[
  {basic, full, candidates},
  basic = Together[Cancel[expr]];
  full = TimeConstrained[
    FullSimplify[basic, assumptions, TimeConstraint -> seconds],
    seconds,
    basic
  ];
  candidates = DeleteDuplicates[{expr, basic, full}];
  First[MinimalBy[candidates, LeafCount]]
];
```

For special-function results, pick one final function basis and audit for leftovers. For example, after converting to GPL, scan for `HPL`, `PolyLog`, `ToGPL`, `GPolyLog`, debug heads, unresolved constants, and unexpected `EulerGamma`.

## Wolfram Reference Grounding

When adapting package or language patterns, check official Wolfram pages first:

- [`Needs`](https://reference.wolfram.com/language/ref/Needs.html) for package loading by context.
- [`BeginPackage`](https://reference.wolfram.com/language/ref/BeginPackage.html) for public and private package contexts.
- [`ParallelMap`](https://reference.wolfram.com/language/ref/ParallelMap.html) and [`ParallelTable`](https://reference.wolfram.com/language/ref/ParallelTable.html) for parallel evaluation behavior and granularity.
- [`FullSimplify`](https://reference.wolfram.com/language/ref/FullSimplify.html) for assumptions, transformation functions, complexity, and time controls.
- [`TimeConstrained`](https://reference.wolfram.com/language/ref/TimeConstrained.html) for bounding expensive operations.
- [`Message`](https://reference.wolfram.com/language/ref/Message.html) and [`Echo`](https://reference.wolfram.com/language/ref/Echo.html) for diagnostics that are cleaner than unconditional `Print`.

## Reproducibility

- Set random seeds with `SeedRandom`.
- Record package versions if available.
- Keep parameter values in one place.
- Avoid relying on notebook state.
- Include a final check cell or test block.
- Parse-check `.wl` scripts with `ToExpression[..., InputForm, HoldComplete]` before running heavy code.
