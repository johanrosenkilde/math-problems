# CLAUDE.md

CLI tool that generates printable PDF math problem sheets for elementary school students (grades 1–6).

## Source structure

```
src/math_problems/
  problems.py   — problem generation (pure Python, no I/O)
  renderer.py   — builds Typst source string, compiles to PDF bytes
  cli.py        — typer entry point, writes math_problems.pdf
tests/
  test_problems.py  — unit tests for generation logic
  test_renderer.py  — tests for Typst source content and PDF output validity
```

## Tech decisions

- **uv** for dependency management and running commands (`uv run math-problems`, `uv run pytest`)
- **typer** for the CLI.
- **Typst** (via the `typst` PyPI package) for PDF generation.
- Typst source is built as a Python f-string in `renderer.py` — no separate `.typ` template file, keeping generation logic in one place