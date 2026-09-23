# Economy: tokens, runtime and storage

Optimise successful, readable calculations per unit cost, not minimum code length at the expense of correctness. The defaults here are design policies, not measured percentage savings or Wolfram requirements.

## Keep three costs separate

Source files consume model context when read or generated. Intermediate algebra consumes kernel memory/runtime. Saved results consume disk and future reload/maintenance effort. Reducing disk bytes alone does not guarantee fewer billed tokens, and using fewer tool calls can be worse if it hides a wrong assumption.

Keep large algebra in the kernel and return the smallest evidence needed to choose the next operation. Do not round, stringify or discard the authoritative expression just to shorten tool output.

## Default persistence policy

**In memory:** cheap substitutions, small lists, simple expansions, plot sampling from an available solution, routine checks and transient diagnostics. These need no export, JSON record or checkpoint.

**Persist:** original/irreplaceable inputs and the user's requested deliverables. Also persist a derived intermediate when it is materially expensive to reproduce and has a named downstream consumer, restart use, or concrete review purpose. A multi-hour reduction needed for master-integral substitution is a plausible checkpoint. A scalar product table rebuilt in a fraction of a second is not. Document a necessary exception, such as a tiny exact input to an external program, in one sentence.

Observe the cost during the calculation, for example:

```wolfram
elapsed = First[AbsoluteTiming[result = calculation;]];
```

Here `calculation` denotes the actual computation to time; it is schematic, not a package API. Do not wrap a previously evaluated result and call that its computation time. [AbsoluteTiming](https://reference.wolfram.com/language/ref/AbsoluteTiming.html) measures elapsed evaluation time.

A useful decision heuristic is:

    expected recomputation avoided > save + reload + validation effort

Apply it only to a result that will actually be reused or reviewed. Include the likelihood of a restart and checkpoint size. There is no universal seconds/megabytes cutoff. Keep expensive results in RAM when that suffices; consider checkpointing before a necessary kernel change or a long interruption.

## Minimal, valid checkpoints

One logical result should have one authoritative saved form, not `.m` + `.mx` + `.wxf` + text + JSON by default. Prefer an already-established project format. `Export`/`Import` with [WXF](https://reference.wolfram.com/language/ref/format/WXF.html) can preserve expression values; they do not automatically reconstruct every function definition, package or live external object needed to use those values. Use readable Wolfram expressions where portability and inspection matter. Do not confuse exporting a symbol's value with saving its definitions.

Use [Save](https://reference.wolfram.com/language/ref/Save.html) or [DumpSave](https://reference.wolfram.com/language/ref/DumpSave.html) only for selected definitions when needed. DumpSave has compatibility limits and does not preserve open streams/links. Never assume it is a complete portable session backup. Treat imported code/definitions as executable content; only load trusted files.

Keep validation metadata with the saved result where the format permits: inputs or their digests, relevant generating-code version, assumptions/conventions, package/kernel versions, precision and the validation actually performed. Include external input hashes and seeds when they affect the result. Check these before reuse; a filename's existence is not validation. Invalidate when any relevant input changes.

Do not hash a huge expression on every step. Compute a key at the expensive persistence boundary, not for transient results. For important checkpoint replacement, write and verify a temporary file before replacing the old good checkpoint. Avoid accumulating timestamped copies; retain earlier versions only when needed for an audit or requested review.

Notebook output cells are also storage. Do not persist a huge raw output in a notebook as well as in a checkpoint. Suppress it before evaluation and retain a compact useful display. Never purge a user's existing outputs or files without establishing that they are disposable and the change is authorised.

## Token policy

Load the core skill, then only the reference relevant to the current uncertainty. Read a symbol's Usage/Details/Possible Issues and one nearest example, not a whole manual. Reuse the evidence for the same version and contract. Record a URL and version in a short existing comment/note rather than repeatedly reciting it.

Read/edit the changed section, not every file in the project. Use targeted diffs. Avoid reposting unchanged code, full logs, all definitions, all diagrams or all master integrals. Do not generate a separate planning document, evidence card, transcript, progress report or summary for each task.

Default routine inspection budget: one relevant property/check and at most three representative terms. If a term is huge, request selected heads or subexpressions instead. Widen only for a named uncertainty; never silently clip an error message or use a clipped sample to establish an identity.

Batch cheap deterministic assignments and independent lookups. Keep real tool-response boundaries at uncertain structures and failed checks. Use one representative computation to discover a transformation, then test genuinely distinct shapes/edge cases before scaling up; one successful sample does not validate every diagram.

Keep a short continuation note only before losing useful context in a long task: file/section, available expensive result, proven contract, unresolved issue and next operation. Reuse an existing note location. Do not create one per turn. Never embed large results in that note.

Do not spawn multiple agents to rewrite the same notebook. Use parallel compute workers for independent ready jobs with bounded transfers and a clear benefit; all agents share one resource budget. No nested `LLMResourceFunction` calls to reformat code or generate comments by default: learn from those prompts without paying for another model call.

## Runtime policy

Prefer a targeted `Collect`, `Factor`, `Cancel`, `Together`, assumption refinement or documented package transformation over repeated global `FullSimplify`. Use only mathematically justified operations. Do not expand before reduction without need. Reuse costly argument-independent values instead of recomputing them through `:=` or plotting.

For an expensive simplification, try a representative case with [TimeConstrained](https://reference.wolfram.com/language/ref/TimeConstrained.html) or appropriate package limits. Inspect failure and change method, rather than automatically escalating timeouts. Maintain adequate precision and regulator orders. Always look for beneficial acceleration, including parallelisation, compilation and temporary memoisation. For independent tasks, use bounded concurrent execution rather than serialising them by habit. Before concurrent or memory-heavy work, follow [parallel runtime](parallel-runtime.md): one CPU/RAM/licence budget, an independent live monitor, controlled admission and output validation. Do not build scaffolding or parallelise cheap work just to satisfy this policy.

## Evaluate the policy fairly

On identical representative tasks, compare with/without this skill: correctness, meaningful checks, readability, source files, duplicated logic, actual available token usage, tool-output volume, execution time and unnecessary persisted bytes. Report measurements only when available. No promised “50% savings,” no inference that fewer files alone means cheaper reasoning, and no skipping physics checks to improve the cost metric.
