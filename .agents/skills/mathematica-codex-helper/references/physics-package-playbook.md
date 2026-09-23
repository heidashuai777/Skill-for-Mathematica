# Physics work: preserve meaning while simplifying

This general skill controls Mathematica style, execution and economy. For an amplitude task, read the installed `ampred-amplitude-calculation` skill when available; its process-specific definitions and checks belong there. A repository URL does not install or invoke that skill. Do not silently edit that repository or duplicate its entire manual here.

## The few conventions that affect the current stage

Record the metric/dimension, external momenta and on-shell conditions, regulator and expansion order, normalisation, integration measure and analytic branch when relevant. Do not recite unrelated conventions for a plotting or algebra task. Never assign a physics dimension to the protected built-in `D`.

The metric signature is not universal across tensor packages or all examples. In particular, xTensor's [DefMetric](https://xact.es/Documentation/HTML/HTMLLinks/xTensor/DefMetric.nb.html) takes signature information as an argument. Read the actual metric definition; do not claim that all xAct calculations use one signature.

## At representation boundaries

Inspect the actual outer form and one representative *complete* small term before writing extraction or replacement rules. Display notation is not an internal expression contract. FeynCalc's [FCI](https://feyncalc.github.io/FeynCalcBook/FCI.html) documents conversion into its internal form; the linked online manual is labelled development-version, so compare against the installed version.

Preserve distinctions between four-dimensional and dimensionally regularised objects; verify the relevant package forms rather than inferring them from a pretty-printed gamma matrix or scalar product. Check that a conversion or replacement acted on the intended structures. An unchanged expression can mean either that no change was needed or that a rule never matched; resolve that ambiguity.

Do not apply commutative simplifications to noncommuting chains. Do not flatten spinor, tensor or colour structures merely because their display looks like a product. Do not use a generic imaginary `polarizationVector[p_] -> momentum[p]` replacement as a real package Ward check. Use the documented actual representation and verify the substituted objects and residual.

## Checks at meaningful boundaries

Choose checks that test the transformation just performed. Examples include a known trace, conservation/on-shell constraints, correct free indices, a normalisation, a differential-equation residual or an applicable symmetry. A full gauge-invariant amplitude may satisfy a Ward identity while individual diagrams do not; identify the object being tested, including required counterterms or contact terms. A manifestly covariant notation alone is not a covariance test.

Distinguish exact equality, a proved identity under assumptions, and numerical agreement. For numerical comparisons use consistent conventions, admissible kinematics, several nonsingular points and sufficient precision. Record a scale-aware absolute/relative tolerance. No blanket `Chop` as proof of a cancellation.

Limits need physical and mathematical justification: taking a mass or collinear invariant to zero can be singular or change which regions contribute. Preserve needed regulators until the intended operation is valid. For Laurent expansions, compute enough orders of *each factor* to account for pole orders in the others. Avoid premature `Normal` when it loses necessary truncation information. Keep the causal prescription and logarithm branches explicit; do not use `PowerExpand` as a universal simplifier.

## Heavy stages and clean state

A costly integration-by-parts reduction, numerical boundary computation or differential-equation solution may deserve a checkpoint when subsequent work needs it. Small kinematic substitutions and routine diagnostics normally do not. Follow [economy](economy.md) for invalidation and precision metadata.

Separate kernels for packages whose current versions actually conflict, or when their documented setup requires it. Do not turn one reported conflict into a universal package claim. A small shared rules file and an expensive hand-off checkpoint can be justified here; one wrapper file for every package function cannot.

When changing a basis, assumptions, external kinematics, loop measure or normalisation, invalidate affected saved results. Do not reuse a cached amplitude solely because its dimensions or filename look plausible. Stop the dependent calculation on failed or inconclusive required checks and repair the first failing stage.
