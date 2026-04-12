#!/usr/bin/env python3
"""Generate a 20×20 multiplication table poster, tiled across 6 A4 pages.

Print all 6 pages and stitch them together in a 3-wide × 2-tall grid
(reading order: left-to-right, top-to-bottom).

Usage:
    uv run python multiplication_table.py
"""

import math
import tempfile
import os
import typst

# Table: 20×20 plus header row/col = 21×21 cells
N = 20
TOTAL = N + 1  # 21

# Tile layout: 3 columns × 2 rows of A4 portrait pages
COLS_PER_PAGE = 7   # 3 × 7 = 21
ROWS_TOP = 11       # top pages: header + rows 1-10
ROWS_BOT = 10       # bottom pages: rows 11-20

FONT_SIZE = "28pt"

# A4 portrait with 5mm margin
MARGIN_MM = 20
PRINTABLE_W = 210 - 2 * MARGIN_MM   # 200mm
PRINTABLE_H = 297 - 2 * MARGIN_MM   # 287mm

# Cell dimensions (subtract 3mm for table stroke overhead, then floor)
CELL_W_MM = math.floor((PRINTABLE_W - 3) / COLS_PER_PAGE * 10) / 10   # 28.1
CELL_H_MM = math.floor((PRINTABLE_H - 3) / ROWS_TOP * 10) / 10       # 25.8


def cell_content(r: int, c: int) -> str:
    if r == 0 and c == 0:
        return "×"
    if r == 0:
        return str(c)
    if c == 0:
        return str(r)
    return str(r * c)


def generate_page(r0: int, r1: int, c0: int, c1: int) -> str:
    cells = []
    for r in range(r0, r1):
        for c in range(c0, c1):
            content = cell_content(r, c)
            if r == 0 or c == 0:
                cells.append(
                    f'table.cell(fill: rgb("#ddd"))'
                    f'[#text(weight: "bold")[{content}]]'
                )
            else:
                cells.append(f"[{content}]")
    return (
        f"#table(\n"
        f"    columns: {c1 - c0} * ({CELL_W_MM}mm,),\n"
        f"    rows: {r1 - r0} * ({CELL_H_MM}mm,),\n"
        f"    align: center + horizon,\n"
        f"    stroke: 0.5pt,\n"
        f"    " + ",\n    ".join(cells) + ",\n"
        f"  )"
    )


def main() -> None:
    row_splits = [(0, ROWS_TOP), (ROWS_TOP, TOTAL)]
    col_splits = [
        (0, COLS_PER_PAGE),
        (COLS_PER_PAGE, 2 * COLS_PER_PAGE),
        (2 * COLS_PER_PAGE, TOTAL),
    ]

    pages = []
    for rs in row_splits:
        for cs in col_splits:
            pages.append(generate_page(*rs, *cs))

    source = (
        f'#set page(paper: "a4", margin: {MARGIN_MM}mm)\n'
        f'#set text(font: "New Computer Modern", size: {FONT_SIZE})\n\n'
        + "\n\n#pagebreak()\n\n".join(pages)
        + "\n"
    )

    with tempfile.NamedTemporaryFile(suffix=".typ", mode="w", delete=False) as f:
        f.write(source)
        tmp = f.name
    try:
        pdf = typst.compile(tmp)
    finally:
        os.unlink(tmp)

    out = "multiplication_table.pdf"
    with open(out, "wb") as f:
        f.write(pdf)
    print(f"Saved {out} (6 pages, arrange 3 wide × 2 tall)")


if __name__ == "__main__":
    main()
