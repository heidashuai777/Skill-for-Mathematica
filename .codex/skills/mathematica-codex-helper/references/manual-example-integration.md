# Manual and Example Integration Protocol

This reference explains how the skill should maximize correct package usage by integrating manuals and examples before generating code.

## Principle

Treat package examples as executable specifications. A package manual is not just background reading; it defines the accepted loading form, argument order, context names, option names, object construction sequence, and expected output shapes.

For physics packages, examples also encode conventions. Those conventions can be as important as the syntax.

## Source Priority

Use sources in this order:

1. Official package documentation and paclet documentation.
2. Official tutorial notebooks and example notebooks.
3. Package test suite and source examples.
4. Repository README and release notes.
5. Maintainer answers or issue discussions.
6. General web examples.
7. Memory, only for stable built-in Wolfram Language syntax.

When sources disagree, prefer the version matching the installed package.

## Package Evidence Card

Create a short evidence card before writing package-dependent code.

```markdown
### Package evidence

- Package:
- Version or source checked:
- Load command:
- Symbols used:
- Manual examples inspected:
- Minimal unchanged example run:
- Adaptation map:
- Important options:
- Conventions:
- Smoke tests:
- Remaining uncertainty:
```

## Example Extraction

For package docs inside a repository, search these paths:

```text
README.md
README.nb
Documentation/
Docs/
Examples/
ExampleNotebooks/
Tutorials/
Tests/
*.wl
*.m
*.nb
```

Use `scripts/extract_wl_examples.py` to extract fenced Mathematica blocks from Markdown files and collect `.wl` examples into JSONL.

## Adaptation Method

1. Find the smallest example that uses the exact symbol needed.
2. Run that example unchanged when possible.
3. Identify all definitions needed before that symbol is called.
4. Make an adaptation map.
5. Change one item at a time.
6. Run a smoke test after each meaningful change.
7. Add physical checks such as dimensions, symmetries, limits, or conservation laws.

Example adaptation map:

```text
manual: manifold M4      -> user: spacetime
manual: coordinates {t,r,theta,phi} -> user: {tau,r,theta,phi}
manual: metric g[-a,-b] -> user: metric[-mu,-nu]
manual: scalar field phi[] -> user: scalarField[]
```

## Validation Layers

Use multiple layers of validation:

### Load checks

```Mathematica
Needs["PackageContext`"]
Names["PackageContext`*"]
```

### Symbol checks

```Mathematica
Information[symbol]
Options[symbol]
SyntaxInformation[symbol]
```

### Example checks

Run the unchanged manual example first. Then run the adapted version.

### Physics checks

Check at least one known limit or invariant. Examples:

- Hermiticity: `hamiltonian == ConjugateTranspose[hamiltonian]`.
- Normalization: `Integrate[Conjugate[psi[x]] psi[x], {x, -Infinity, Infinity}] == 1`.
- Tensor symmetry: compare the expected index permutations.
- Flat-space limit: set curvature parameters to zero.
- Classical limit: take `hbar -> 0` only when mathematically meaningful.

## Anti-Hallucination Rules

- Never guess a context string for a package. Verify it from the manual or package files.
- Never guess option names. Inspect `Options[symbol]` or examples.
- Never assume package examples use the same conventions as the user's problem.
- Never mix syntax from two packages unless the manual explicitly supports it.
- Never hide uncertainty. Mark uncertain package behavior clearly.

## User-Facing Summary

In final answers, keep the manual evidence short:

```markdown
I followed the package's documented pattern:
- load package
- define domain objects
- call main symbol with documented argument order
- verify with a minimal smoke test
```

Avoid copying long manual text. Summarize instead.
