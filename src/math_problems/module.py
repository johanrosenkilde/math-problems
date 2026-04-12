from abc import ABC, abstractmethod
from typing import Any


_BASE_PREAMBLE = """\
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
#set text(font: "New Computer Modern")
"""


# ---------------------------------------------------------------------------
# Shared helpers for page layout and Typst code generation
# ---------------------------------------------------------------------------

def build_page_layout(
    title: str,
    problem_calls: str,
    answers: list[tuple[int, int | float]],
    *,
    header: str = "",
    header_spacing: str = "0.8cm",
    columns: str = "(auto, auto, auto)",
    rows: str | None = None,
    column_gutter: str = "2.5cm",
    row_gutter: str = "1.6cm",
    grid_align: str | None = None,
    center_grid: bool = True,
    answer_separator: str = "#h(1cm)",
    answer_size: str = "12pt",
) -> str:
    """Standard page layout: title → optional header → 3×3 problem grid → answer footer."""
    answer_text = answer_separator.join(f"{n}. {r}" for n, r in answers)

    # Header between title and grid
    if header:
        header_section = f"\n{header}\n"
    else:
        header_section = f"\n#v({header_spacing})\n"

    # Build grid attribute lines
    grid_attrs = [f"columns: {columns},"]
    if rows:
        grid_attrs.append(f"rows: {rows},")
    grid_attrs.append(f"column-gutter: {column_gutter},")
    grid_attrs.append(f"row-gutter: {row_gutter},")
    if grid_align:
        grid_attrs.append(f"align: {grid_align},")
    grid_attrs.append(problem_calls)
    grid_body = "\n    ".join(grid_attrs)

    if center_grid:
        grid_section = f"#align(center)[\n  #grid(\n    {grid_body}\n  )\n]"
    else:
        grid_section = f"#grid(\n    {grid_body}\n  )"

    return (
        f"#align(center)[\n"
        f"  #text(size: 24pt, weight: \"bold\")[{title}]\n"
        f"]\n"
        f"{header_section}\n"
        f"{grid_section}\n"
        f"\n"
        f"#v(1fr)\n"
        f"\n"
        f"#align(center)[\n"
        f"  #text(size: {answer_size})[{answer_text}]\n"
        f"]"
    )


def arithmetic_preamble(operator: str) -> str:
    """Typst preamble for a two-operand vertical arithmetic problem."""
    return (
        "#let problem(num, a, b) = context {\n"
        "  let inner = grid(\n"
        "    columns: (auto, auto),\n"
        "    column-gutter: 0pt,\n"
        "    row-gutter: 18pt,\n"
        "    align: (left, right),\n"
        "    [], text(size: 40pt)[#a],\n"
        f"    text(size: 40pt)[{operator}], text(size: 40pt)[#b],\n"
        "  )\n"
        "  let w = measure(inner).width\n"
        "  let lbl = text(size: 14pt, weight: \"bold\")[#num.]\n"
        "  let lw = measure(lbl).width\n"
        "  box({\n"
        "    place(dx: -lw - 4pt, lbl)\n"
        "    v(10pt)\n"
        "    inner\n"
        "    v(2pt)\n"
        "    line(length: w, stroke: 1.5pt)\n"
        "    v(30pt)\n"
        "    line(length: w, stroke: 1.5pt)\n"
        "    v(-8pt)\n"
        "    line(length: w, stroke: 1.5pt)\n"
        "    v(1cm)\n"
        "  })\n"
        "}\n"
    )


# ---------------------------------------------------------------------------
# Module ABC
# ---------------------------------------------------------------------------

class Module(ABC):
    @property
    @abstractmethod
    def slug(self) -> str:
        """Short identifier used in CLI (e.g. 'addition')."""

    @abstractmethod
    def title(self, locale: str) -> str:
        """Display name used as the page headline, in the given locale."""

    @abstractmethod
    def generate(self, n: int, difficulty: int) -> list[Any]:
        """Generate n problems at the given difficulty level."""

    @abstractmethod
    def typst_preamble(self) -> str:
        """Typst source: page/text setup + let-bindings for this module."""

    @abstractmethod
    def page_source(self, problems: list[Any], start_num: int, locale: str) -> str:
        """Typst markup for a single page of up to 9 problems."""
