# Output-driven development without output flooding

The goal is decision-making from evaluated expressions, not ritual inspection after every assignment. Outlining future mathematical stages is fine. Committing to unobserved expression structure is not.

## A real execution gate

A new package call is an execution boundary. Send the current step to the available Wolfram evaluator and **wait for its response**. Read that response before writing a rule or extraction that depends on it. Do not put both the speculative extraction and its “inspection” in one uninterrupted call.

In a persistent session, start with a saved result:

```wolfram
(* raw has already been assigned by the documented package call. *)
{Head[raw], Short[raw, 3]}
```

Then, in a separate tool interaction, choose an inspection based on the actual head. For an observed list, ask for `Length[raw]` and at most a few elements. For an observed matrix, ask for `Dimensions[raw]`. For an association, inspect relevant keys. For a package wrapper, read its documented accessors or inspect a small internal example. Do not blindly use `raw[[1,2,3]]`.

If a list of rules was observed and the next step requires rules, check that contract before replacement. If a purported result is the original unevaluated function call, diagnose loading, argument shape or assumptions; the absence of an error message is not success.

An adequate observation is one line: actual result type, a property relevant to the decision, and whether the required check passed. Keep it in the tool exchange; retain a brief source comment only when it explains a lasting decision. Do not create a stage report file.

## Inspection should answer a question

Use `Head` to identify an outer form. Use a bounded sample to understand a structure. Use `Cases[expr, verifiedPattern, levels, n]` for at most `n` relevant matches when that is the needed question. A negative conclusion about the *whole* expression requires a full appropriate predicate, not an absent match in a sample.

`Length` counts arguments of the current head, not universal terms. If a top-level additive count is actually useful:

```wolfram
termCount = Which[
  expr === 0, 0,
  Head[expr] === Plus, Length[expr],
  True, 1
];
```

This counts unexpanded top-level terms only. Do not expand solely to count them. `Variables` is not a general dependency finder for tensors, spinor chains or transcendental expressions. `FullForm`, `TreeForm`, unrestricted `Cases`, `LeafCount` and `ByteCount` can themselves be costly; use only those that answer the present question. Inspect a small subexpression before an entire amplitude.

`Short[expr,3]` is approximately three display lines, not a strict three-line or token cap. A plain-text tool can use `ToString[Short[expr,3],OutputForm]`; when even formatting is expensive, inspect metadata or a bounded subexpression instead. The truncated view is evidence about what was displayed, never a substitute for the full kernel expression. See [Short](https://reference.wolfram.com/language/ref/Short.html).

## Reuse the kernel, not invisible assumptions

Use a persistent local evaluator when it already exists. Keep named intermediates available and do not restart between ordinary sections. Record `$Version` and the relevant package versions once per session; recheck after a restart or package change. A session retains definitions and cached state, not guaranteed correctness. Re-execute downstream dependants after any upstream edit.

If only fresh processes are available, replay the same small validated prefix plus the next stage, preferably by selecting cells/sections using existing tooling. A one-shot `wolframscript` call does not remember a previous process. Reuse a qualified expensive checkpoint when replay would be wasteful; rebuild the cheap prefix. Do not create a server, IPC protocol or a new runner per cell merely to imitate a notebook.

After discovery, consolidate the working route. Validate it from a fresh kernel when feasible. For a very expensive route, validate its cheap path and checkpoint resume path; say explicitly when a full fresh run was not performed. Do not silently restart a day-long calculation solely to obtain a green badge.

## Fix before proceeding

Keep the failing input, actual message and one bounded problematic subexpression. Compare against the smallest relevant documented example. Test one correction at a time. Revert a failed correction rather than layering new assumptions on it. Isolate package conflicts in separate kernels only when observed or documented for the versions used.

A timeout, `$Failed`, `$Aborted`, unresolved contract, or unexpected unevaluated call blocks dependent work. Some messages are documented and harmless; recognise those specifically rather than using blanket `Quiet`. A changed representation needs a new inspection, not a guessed replacement rule.

For exact checks, distinguish `True`, `False` and a remaining symbolic condition. Only `True` establishes a passed Boolean contract; `TrueQ` alone cannot tell failure from inconclusiveness. Numeric tests need stated tolerances, scale and precision. Wolfram's [VerificationTest](https://reference.wolfram.com/language/ref/VerificationTest.html) supports expected results and messages, but a test must actually execute and its outcome must be read.

## No execution available

Do static edits and documented code where the interface is established. Label unexecuted work once. Separate an analytic expectation from an observed kernel result. Stop speculative output-dependent stages at the first unknown contract and request only that stage's minimal diagnostic output if needed. Do not claim a Python algebra check, syntax scan, screenshot, or saved notebook output proves a Mathematica package ran.

The skill never grants execution access. Run inspection automatically when an evaluator is available; do not ask the user to approve each safe cell or to copy results that you can read yourself.

## Concurrent branches still require observations

Independent ready branches may run in parallel under the [shared resource policy](parallel-runtime.md). A wait at an unresolved dependent step blocks that branch, not unrelated work. Read each actual completed result and its messages before choosing its next operation. Give independent programs isolated mutable state; do not evaluate two simultaneous mutations of the same notebook/kernel. An OS-level monitor must remain responsive while kernels compute or wait. Reuse the original sectioned source; parallel tasks do not require parallel source copies.
