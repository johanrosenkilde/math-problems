import random
from pathlib import Path

import typer

from math_problems.addition import AdditionModule
from math_problems.counting_squares import CountingSquaresModule
from math_problems.division import DivisionModule
from math_problems.multiplication import MultiplicationModule
from math_problems.renderer import render_pdf
from math_problems.subtraction import SubtractionModule
from math_problems.grocery_list import GroceryListModule

MODULES = [AdditionModule(), SubtractionModule(), MultiplicationModule(), DivisionModule(), CountingSquaresModule(), GroceryListModule()]
MODULE_MAP = {m.slug: m for m in MODULES}

app = typer.Typer()


@app.command()
def main(
    output: Path = typer.Option(
        Path("math_problems.pdf"), "--output", "-o", help="Output PDF path."
    ),
    pages: int = typer.Option(1, "--pages", "-p", help="Number of pages to generate."),
    difficulty: float = typer.Option(
        1, "--difficulty", "-d", help="Difficulty level (1–3, half-steps like 1.5 supported by some modules)."
    ),
    module: str = typer.Option(
        None, "--module", "-m", help=f"Comma-separated problem types to use: {', '.join(MODULE_MAP)}. Defaults to all."
    ),
    locale: str = typer.Option(
        "da", "--locale", "-l", help="Language for PDF titles: en, da."
    ),
) -> None:
    """Generate a PDF with 9 problems per page, randomly mixing problem types."""
    if module is not None:
        names = [m.strip().lower() for m in module.split(",")]
        invalid = [n for n in names if n not in MODULE_MAP]
        if invalid:
            raise typer.BadParameter(f"Unknown module(s): {', '.join(invalid)}. Choose from: {', '.join(MODULE_MAP)}")
        pool = [MODULE_MAP[n] for n in names]
    else:
        pool = MODULES
    page_data = []
    for _ in range(pages):
        selected = random.choice(pool)
        try:
            problems = selected.generate(n=9, difficulty=difficulty)
        except ValueError as e:
            raise typer.BadParameter(str(e))
        page_data.append((selected, problems))
    pdf_bytes = render_pdf(page_data, locale)
    output.write_bytes(pdf_bytes)
    typer.echo(f"Saved {output} ({pages} page{'s' if pages != 1 else ''})")
