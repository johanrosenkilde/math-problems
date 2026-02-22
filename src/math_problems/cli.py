import random
from pathlib import Path

import typer

from math_problems.addition import AdditionModule
from math_problems.multiplication import MultiplicationModule
from math_problems.renderer import render_pdf
from math_problems.subtraction import SubtractionModule

MODULES = [AdditionModule(), SubtractionModule(), MultiplicationModule()]

app = typer.Typer()


@app.command()
def main(
    output: Path = typer.Option(
        Path("math_problems.pdf"), "--output", "-o", help="Output PDF path."
    ),
    pages: int = typer.Option(1, "--pages", "-p", help="Number of pages to generate."),
    difficulty: int = typer.Option(
        1, "--difficulty", "-d", help="Difficulty level (1–3)."
    ),
) -> None:
    """Generate a PDF with 9 problems per page, randomly mixing problem types."""
    page_data = []
    for _ in range(pages):
        module = random.choice(MODULES)
        try:
            problems = module.generate(n=9, difficulty=difficulty)
        except ValueError as e:
            raise typer.BadParameter(str(e))
        page_data.append((module, problems))
    pdf_bytes = render_pdf(page_data)
    output.write_bytes(pdf_bytes)
    typer.echo(f"Saved {output} ({pages} page{'s' if pages != 1 else ''})")
