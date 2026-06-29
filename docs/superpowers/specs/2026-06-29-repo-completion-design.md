# Repo Completion Design

## Goal

Finish the public repository packaging around the Mathematica Codex Helper skill so it is installable, validated, licensed, and releasable as `v0.2.0`.

## Scope

- Add an MIT license.
- Add GitHub Actions validation for the Python tests, JSON manifest, and synchronized skill files.
- Add `agents/openai.yaml` UI metadata for the skill.
- Add contribution and security guidance at the repository root.
- Add changelog notes for `v0.2.0`.
- Update the README with release, license, and validation information.
- Add a repo-completion validation script so these publication artifacts remain present.

## Design

The repository remains a small Codex skill package. The skill itself stays in `.codex/skills/mathematica-codex-helper`, helper automation stays in `scripts/`, validation stays in `tests/`, and public project metadata stays at the repository root. CI runs only local, deterministic checks and does not require Wolfram credentials or networked Wolfram services.

## Success Criteria

- Local validation passes.
- GitHub Actions has a `Validate` workflow.
- PR #1 is ready to merge and targets `main`.
- `main` receives the completion changes.
- GitHub release `v0.2.0` exists after merge.
