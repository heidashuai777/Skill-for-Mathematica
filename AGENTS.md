# Maintaining this skill repository

The canonical skill is `.agents/skills/mathematica-codex-helper/SKILL.md`.
Keep exactly one skill definition; no lowercase or legacy duplicate.

This is an instruction library, not a runtime framework. Keep the core below
850 whitespace-delimited words. Put specific detail in the existing references
and load those only when relevant. Maintain the notebook-first, observed-output,
one-calculation-file, selective-checkpoint and no-summary defaults. Keep the shared
CPU/RAM/licence budget, independent live memory monitoring and observed-output
gates compatible with concurrency. Do not make a new .wl source per worker. Do not add
runners, logging systems, package installers, generated reports or many templates.

Preserve necessary physics and package accuracy. Cite version-aware primary
sources with normal links; no conversation-specific citation IDs. Never label
static checks as Mathematica execution or claim token savings without measurement.

Run `python3 tests/check_skill.py` after editing. It checks structure and the
bundled example's lexical balance, not Wolfram syntax or physics correctness.
Evaluate the example in a real Wolfram kernel when one is available. Do not install
or activate a paid runtime automatically. Keep the final hand-off to changed paths,
actual test status and any blocker; no generic recap.
