# Contributing

This repository packages a Codex skill for Mathematica / Wolfram Language and physics workflows.

## Development workflow

1. Create a branch from `main`.
2. Keep `SKILL.md` and `skill.md` synchronized.
3. Add or update tests for any helper script, manifest, or repository contract change.
4. Run the validation commands before opening or updating a pull request.

## Validation

Run:

```bash
python -B tests/validate_resource_scaffold.py
python -B tests/validate_repo_completeness.py
python -B -m unittest discover -s tests
python -B -c "import json; json.load(open('data/wolfram-resource-manifest.json', encoding='utf-8')); print('json ok')"
diff -q .codex/skills/mathematica-codex-helper/SKILL.md .codex/skills/mathematica-codex-helper/skill.md
```

## Skill guidance

- Keep the main skill concise.
- Put detailed operational guidance in `references/`.
- Treat manifest entries as candidate resources until verified.
- Do not commit Wolfram credentials, private notebooks, generated caches, or proprietary source snippets.
