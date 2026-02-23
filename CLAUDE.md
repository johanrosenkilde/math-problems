# CLAUDE.md

CLI tool that generates printable PDF math problem sheets for elementary school students (grades 1–6).

## Source structure

```
src/math_problems/
  module.py      — Module ABC (title, generate, typst_preamble, page_source)
  addition.py        — AdditionProblem dataclass + AdditionModule
  subtraction.py     — SubtractionProblem dataclass + SubtractionModule
  multiplication.py  — MultiplicationProblem dataclass + MultiplicationModule (asymmetric difficulty ranges)
  division.py        — DivisionProblem dataclass + DivisionModule (same ranges as multiplication; divisor ≥ 2, result always integer)
  renderer.py        — build_typ_source(pages), render_pdf(pages)
  cli.py         — typer entry point, writes math_problems.pdf
tests/
  test_addition.py       — unit tests for AdditionProblem and AdditionModule
  test_subtraction.py    — unit tests for SubtractionProblem and SubtractionModule
  test_multiplication.py — unit tests for MultiplicationProblem and MultiplicationModule
  test_division.py       — unit tests for DivisionProblem and DivisionModule
  test_renderer.py       — tests for Typst source content and PDF output validity
```

## Adding a new problem type

1. Create `src/math_problems/<type>.py` with a `<Type>Problem` dataclass and `<Type>Module(Module)`.
2. Add `tests/test_<type>.py` mirroring the structure of `test_addition.py`.

## Tech decisions

- **uv** for dependency management and running commands (`uv run math-problems`, `uv run pytest`)
- **typer** for the CLI.
- **Typst** (via the `typst` PyPI package) for PDF generation.
- Typst source is built as a Python f-string in `renderer.py` — no separate `.typ` template file, keeping generation logic in one place

## Workflow

- Never suggest or initiate a git commit. Only commit when explicitly asked. Add and commit in the same suggested command.
- Always update CLAUDE.md whenever relevant changes happen, or when you learn new things about what you should and should not do.
- Never implement features or changes that weren't explicitly requested. If a request isn't possible with the current code, say so and suggest options — do not implement them unilaterally.