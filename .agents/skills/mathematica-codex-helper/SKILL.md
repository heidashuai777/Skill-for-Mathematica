---
name: mathematica-codex-helper
description: Write, review, or debug Mathematica/Wolfram Language research calculations in a sectioned, notebook-first style. Use for symbolic work and physics packages; route full QFT scattering-amplitude pipelines to `ampred-amplitude-calculation`. Prioritise actual outputs, few files, selective checkpoints, resource-aware parallelism and low token overhead.
---

# Mathematica: notebook-first research

Write like a Mathematica researcher, not an application generator. Keep the mathematical argument visible.

## Defaults

- **One authoritative calculation.** Continue the existing `.nb`, `.m`, or `.wl`. For a new task, start with one sectioned calculation file. Add another only for a real reuse, package-isolation, or resource boundary; explain that reason in one sentence. Never create one file per stage, `final_v2` copies, or a framework by default.
- **Sections, not scaffolding.** Use native Section/Subsection cells in notebooks. In text use `(* ::Section:: *)` followed by `(*Section name*)`. Name sections by mathematics: Kinematics, Trace, Reduction, Boundary conditions. Omit irrelevant sections. No generated Summary section or report.
- **Direct expressions first.** Use named intermediate results, short rules, and small mathematical functions near first use. Introduce helpers only for genuine repeated work or a clearer mathematical operation. Do not predefine speculative transformation functions. Prefer short conventional names to verbose application-style identifiers. Avoid `Module`/`With` wrappers around exploratory sections; use proper local scoping when reusable code actually needs it.
- **Sparse output.** Suppress large assignments with `;`, then explicitly return one useful result or bounded inspection. No routine `Print` narration, per-step logs, or automatically exported diagnostics.

## Develop through observed results

**Write → evaluate → inspect → decide → fix or continue.**

1. Inspect the current section and relevant existing definitions. State only conventions that affect this calculation. Identify the available kernel/session and loaded package versions; do not assume execution access.
2. Write and evaluate the smallest unresolved step. Batch independent cheap work, but stop at a new package representation, branch, failure, or physics-sensitive transformation.
3. Read the actual tool result before authoring dependent transformations. Inspect the property needed for the next decision: a head, dimensions of an actual array, a bounded example, or a check. A guessed result, saved notebook output, or comment saying “inspect here” is not runtime evidence.
4. Advance only when the required contract/check passes. On unexpected output, fix the first failing step and rerun affected dependants. An unresolved symbolic condition is **inconclusive**, not success. Keep the last good expensive result until its replacement passes.
5. Once a route works, consolidate that route into readable sections; remove your dead helpers and temporary diagnostics. Reuse validated straight-line code. Do not force interactive pauses for already-established operations.

Prefer a persistent kernel. If only fresh-process execution is available, replay a small validated prefix plus the next step in the same file, using a justified expensive checkpoint when necessary. Do not build a kernel service or file-per-cell runner. Without a kernel, label code **unexecuted** and leave output-dependent work unresolved; never fabricate observed results.

## Accelerate within a shared budget

Always seek safe runtime improvements. Run independent ready tasks concurrently when beneficial, using a bounded subkernel pool or separate existing programs. Profile a representative case; budget all masters, subkernels and native threads together. Monitor OS-level memory during execution, including children and result assembly. Reserve headroom, stop new admissions under pressure, and manage only task-owned processes. Never parallelise dependent, unvalidated steps or sacrifice correctness. Read [parallel runtime](references/parallel-runtime.md) before concurrent or memory-heavy work.

## Save selectively

Keep cheap derived expressions in memory, not on disk. Save requested deliverables and irreplaceable inputs. Save an intermediate only when recomputation is materially expensive **and** a next step, restart, or specific review needs it. Measure expensive steps once; do not time them by rerunning them. Reuse one checkpoint with sufficient inputs, conventions, code/package versions and precision to invalidate stale results. No automatic whole-session dumps, per-stage JSON, duplicate formats, or notebook output copies of huge cached expressions. Do not delete user data.

## Spend tokens on decisions

Read only relevant sections, source examples and diffs. Return compact observations, not full expressions or repeated code. Never expand an expression merely to inspect it. Keep large algebra in the kernel; request bounded subexpressions. Reuse established evidence until its version or contract changes. No mandatory plans, evidence reports, change reports, or final recaps. Final delivery: changed path, actual result or test status, and a blocker only when present. Explain derivations when requested or needed for a non-obvious step.

## Correctness is not optional

Verify unfamiliar package loaders, signatures, options and conventions against version-matching primary sources and a small example. Metadata inspection is not execution. Keep computation separate from `Short`/`MatrixForm` display wrappers. Use exact inputs and explicit assumptions; preserve regulator order and analytic branches. Inspect before positional extraction or structural replacement. No blanket `Quiet`, global clearing, or treating a numerical spot check as proof.

## Route full amplitude pipelines

For scattering amplitudes using AmpRed, FeynCalc, loop-integral reduction, or master-integral assembly, use the `ampred-amplitude-calculation` skill for its domain-specific workflow.

## Read more only when needed

- Layout/refactoring: [Wolfram style](references/wolfram-style-guide.md).
- Execution/inspection failure: [interactive workflow](references/interactive-workflow.md).
- Storage, runtime or token cost: [economy](references/economy.md).
- New package or source lookup: [manual/example integration](references/manual-example-integration.md).
- Amplitudes/tensors/physics: [physics checks](references/physics-package-playbook.md). Use the installed ampred skill for its domain-specific contracts, without duplicating these general rules.
