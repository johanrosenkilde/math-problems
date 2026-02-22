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
    pages: int = typer.Option(1, "--pages", "-p", help="Number of pages to generate."),
) -> None:
    """Generate a PDF with 9 addition problems per page."""
    problems = generate_addition_problems(n=9 * pages)
    pdf_bytes = render_pdf(problems)
    output.write_bytes(pdf_bytes)
    typer.echo(f"Saved {output} ({pages} page{'s' if pages != 1 else ''})")
