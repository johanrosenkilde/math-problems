from pathlib import Path

import typer

from math_problems.problems import generate_addition_problems
from math_problems.renderer import render_pdf

app = typer.Typer()


@app.command()
def main(
    output: Path = typer.Option(
        Path("math_problems.pdf"), "--output", "-o", help="Output PDF path."
    ),
) -> None:
    """Generate a single-page PDF with 9 addition problems."""
    problems = generate_addition_problems()
    pdf_bytes = render_pdf(problems)
    output.write_bytes(pdf_bytes)
    typer.echo(f"Saved {output}")
