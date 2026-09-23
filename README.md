# Mathematica: notebook-first research

A Codex skill for Mathematica/Wolfram Language calculations that read like a
researcher's notebook: direct mathematics, clear sections, actual intermediate
outputs and a small number of useful files.

**Write → evaluate → inspect → decide → fix or continue.**

The default deliverable is one authoritative `.nb`, `.m` or `.wl` calculation,
not a generated application. No automatic Summary section, stage report files,
helper-function forest, or disk copy of every intermediate expression.

## Use it

The canonical skill is [SKILL.md](.agents/skills/mathematica-codex-helper/SKILL.md).
Current Codex documentation specifies `.agents/skills` for repository-local
skills and `~/.agents/skills` for user-level skills. This version replaces the
legacy `.codex/skills` copies with one uppercase `SKILL.md`; keeping two same-name
skills does not merge their instructions. See [OpenAI's skill documentation](https://developers.openai.com/codex/skills).

Open this repository in your Codex workspace, then include the skill in a prompt:

```text
$mathematica-codex-helper
Continue my calculation in its existing file. Use mathematical sections,
read the actual result at uncertain steps, and save only useful expensive
intermediates. No Summary section or extra helper files.
```

In Codex CLI/IDE, `/skills` or `$` can select a skill. Typing `$` is not a shell
command or an automatic installer. Codex can also select a skill by its description;
explicit invocation is useful for a first test. Changes are normally detected
automatically; restart if the updated skill does not appear.

For another research project, copy **only** the
`.agents/skills/mathematica-codex-helper` directory into that project's
`.agents/skills/`, or install that directory once under `~/.agents/skills/`.
Keep its references and example with it. Do not copy this entire repository's
maintenance files into each calculation. Avoid an old user-level installation
shadowing or duplicating the new version.

This skill supplies instructions, not Mathematica, package installations, a
licence or a persistent kernel. Codex must use the actual evaluator available
in its execution environment. Without one it can edit code, but must label it
unexecuted rather than inventing intermediate outputs.

## What changes in practice

| Default | Behaviour |
| --- | --- |
| Organisation | One calculation; mathematical sections |
| New functions | Mathematical meaning or real reuse |
| New files | Explicit reuse/isolation/resource reason |
| Execution | Observe before dependent decisions |
| Acceleration | Independent tasks; bounded shared resources |
| Memory safety | Live host/process monitoring; selective limits |
| Display | Relevant result or bounded sample |
| Persistence | Deliverables, original inputs, costly reusable results |
| Documentation | Version-matching example on demand |
| Final response | Changed path and actual test status |

The one-file default is not a ban on reusable packages. A real shared rules file,
an incompatible-package boundary or an independent expensive computation can
justify another file. Neither one file nor short code is an excuse to hide
mathematics inside a giant function.

## Acceleration and concurrent programs

The skill now requires Codex to look for runtime improvements, not merely write
parallel-looking code. Independent ready jobs should run concurrently when their
CPU, memory and licence allocations fit. Use a bounded Mathematica subkernel pool
or separate existing programs; do not generate one `.wl` copy per worker.

[Parallel runtime](.agents/skills/mathematica-codex-helper/references/parallel-runtime.md)
specifies one shared budget across masters, subkernels and native external workers,
peak-memory estimates, result-assembly headroom and an OS-level monitor that stays
responsive while Mathematica is busy. It distinguishes adaptive admission from
hard operating-system containment. Package state, actual outputs and precision
must remain correct. Small tasks need not be parallelised when overhead dominates.

```text
$mathematica-codex-helper
Accelerate this calculation and run independent tasks concurrently.
First inspect the actual host's CPU, available RAM and kernel limits.
Use one shared budget and live memory monitoring, reduce concurrency under
pressure, and inspect each completed result before dependent work.
Keep the existing mathematical sections; no cloned programs or Summary section.
```

This is an instruction policy, not a bundled scheduler or a claim that a monitor
is already running. Codex must use available local process/evaluator tools and
verify their operation. It must not fabricate hardware capacities, a speed-up,
or protection that its execution environment cannot provide.

## Wolfram patterns used

The design draws on specific published examples, not just generic advice to
“be readable.” [The source notes](.agents/skills/mathematica-codex-helper/references/manual-example-integration.md)
connect Quantum Framework evolution, a stress/strain calculation, Euler equations,
temporary caching and Wolfram's formatting/name/comment prompts to the rules.
They distinguish observed example presentation from this project's own policies.
Prompts are design references, not extra paid model calls or proof of correctness.

## Files you may read

```text
.agents/skills/mathematica-codex-helper/
  SKILL.md
  references/
    wolfram-style-guide.md
    interactive-workflow.md
    economy.md
    parallel-runtime.md
    manual-example-integration.md
    physics-package-playbook.md
  examples/
    gaussian-ground-state.wl
```

Only the core is needed initially. Read a reference when its topic is relevant,
not the whole directory for every task. The single built-in-only worked example
shows sectioned retained code; it is not a package-specific runtime benchmark.

For scattering amplitudes, use this general style policy alongside the installed
`ampred-amplitude-calculation` skill for domain-specific contracts. Neither skill
can infer a package's actual output without running and inspecting it.

## Maintaining and checking the skill

```bash
python3 tests/check_skill.py
```

This standard-library check validates the small distribution, relative links,
core size, duplicate skill names and lexical balance of the example. It does
**not** parse Wolfram Language or certify physical results. In Mathematica,
evaluate the example section by section. Its analytic expected final result is
`{1, hbar/(2 m omega), hbar omega/2}` under its positive-parameter assumptions;
that expectation is not a statement that it ran in a particular environment.

To assess behaviour rather than merely file structure, try these tasks:

- Refactor a trivial multi-file calculation into one sectioned source while preserving a genuinely reused rules file.
- Present a new package result with an unexpected head; Codex must inspect it before inventing an extraction.
- Compare a cheap substitution with a reusable hours-long reduction; only the latter normally merits a checkpoint.
- Remove execution access; Codex must not claim an observed output or fabricate a passing test.
- Provide independent jobs plus one dependent branch; Codex should admit independent work within one resource budget, monitor descendants, and keep dependent work gated.
- Simulate low memory or a failed child; new launches should stop and partial/stale outputs must not be promoted.
- Request a reusable library explicitly; Codex must use appropriate scoping instead of applying the exploratory default blindly.

Keep these checks practical. Measure available token usage, runtime, output volume,
readability and correctness on comparable tasks before claiming improvements.
Do not add dependencies, bulk documentation downloads or a heavy CI pipeline just
to maintain an instruction-only skill.
