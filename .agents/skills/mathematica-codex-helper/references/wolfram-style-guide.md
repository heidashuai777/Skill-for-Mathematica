# Wolfram-native research style

Read this for layout decisions or a refactor, not on every step. The primary-source examples behind these choices are recorded in [manual/example integration](manual-example-integration.md).

## The calculation is the organising unit

A notebook is a mathematical workspace. Use Section cells for conceptual stages, Input cells for executable work and brief Text cells for assumptions or a non-obvious identity. Do not encode headings as `Print` output. Section/Subsection cell grouping is supported by Wolfram's [CellGrouping documentation](https://reference.wolfram.com/language/ref/CellGrouping.html).

Text `.m`/`.wl` sources should remain easy to scan without a front end:

```wolfram
(* ::Section:: *)
(*Kinematics*)

assumptions = s > 0 && 0 < z < 1;
kinematicRules = {s1 -> s z, s2 -> s (1 - z)};

(* ::Section:: *)
(*Invariant relation*)

invariant = (s1 + s2) /. kinematicRules;
Simplify[invariant == s, Assumptions -> assumptions]
```

This is a small self-contained algebra example, not a model of a complete amplitude. The un-suppressed final expression is useful notebook output. A batch evaluator must explicitly capture its return value: running a file successfully is not evidence that every intermediate result was displayed.

Preserve an existing notebook as the authority. A text-only editor should not rewrite thousands of notebook boxes. Use the existing text companion if it is authoritative; otherwise make a targeted notebook change through supported notebook tools. Do not create a second divergent implementation. A new text calculation can later be opened/converted in Mathematica; do not generate raw box structures as a default workflow.

## Names and definitions

Use `ampRaw`, `amp`, `kinRules`, `masters`, `boundary`, `eqs`, `sol`, `s`, `z`, `eps` when those are clear in the project. Use a short notation key where needed. Do not mechanically rename mathematical notation to `processedAmplitudeTransformationResult` or use arbitrary names such as `data1` everywhere.

Keep short functions that express mathematics. A wavefunction `psi[x_] := ...` is sensible even when used once. A one-line wrapper around every built-in is not. Extract a helper after repeated logic or a stable useful interface appears, not after an arbitrary line count. Preserve good existing APIs.

Use `=` for a result that should be computed now and reused. Use `:=` when re-evaluation with arguments is intended; avoid putting expensive argument-independent work inside delayed definitions. Do not introduce a large `Module`, `With`, `Block`, association registry or callback system to hide ordinary exploratory intermediates. Proper scoping remains appropriate inside real reusable functions and packages.

Keep definitions before their first use, close to the relevant mathematics, rather than placing every hypothetical helper at the top. A validated library may legitimately have many definitions; the default is different for a one-off calculation.

## Mathematical clarity and state

Use built-ins and package-native forms rather than recreating them. Short `Map`, `Table`, rules and pure functions are idiomatic; deep nested slot expressions are not a requirement for elegance. Break a transformation chain at its conceptual boundaries.

Pass assumptions to the operation that needs them, including `Integrate`, rather than only simplifying afterwards. Keep exact rational input until numerical work begins. Do not assign to protected built-ins such as `D`, `I`, `N`, or `E`. Use `dim` for a dimension variable outside a package's documented conventions. Avoid computational `Subscript` variables and history references such as `%` in retained code.

Keep display separate:

```wolfram
matrix = {{1, 0}, {0, -1}};
matrix // MatrixForm
```

Do not assign the `MatrixForm` wrapper to `matrix`. Similarly, store the full expression first and shorten only its display. Wolfram documents this pitfall for [Short](https://reference.wolfram.com/language/ref/Short.html).

Clear only the user-owned symbols being redefined. Rerun downstream sections after changing parameters, assumptions or definitions. Do not clear a package or a whole user's session. Keep path configuration in one place; do not impose `NotebookDirectory[]` on a headless process or a machine-specific home directory on a portable script.

## Refactor in place

First establish what the existing calculation actually does. Consolidate trivial stage files into conceptual sections of the authoritative file; update callers. Retain separate files for truly reusable rules, incompatible package kernels, independent expensive jobs, or explicitly requested reusable packages. Preserve original inputs, requested results, expensive checkpoints, provenance and externally referenced filenames.

Delete only your own obsolete duplicates, and only after verifying their replacement. No `summary.wl`, `REPORT.md`, `FINAL_SUMMARY.md`, audit dump, README or changelog per scientific task unless requested. Tests and explanatory comments belong near the relevant calculation; a real maintained library can justify its own test suite.
