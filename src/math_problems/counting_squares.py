import random
from dataclasses import dataclass

from math_problems.module import Module


_DIFFICULTY_SETTINGS: dict[int, tuple[int, int, int]] = {
    1: (5,  6, 12),
    2: (6, 10, 18),
    3: (10, 30, 60),
}

_PREAMBLE = """\
#let problem(num, n, cells) = {
  let cell_size = if n <= 5 { 0.7cm } else if n == 6 { 0.6cm } else { 0.45cm }
  let draw_cell(c) = if c == 1 {
    box(width: cell_size, height: cell_size, fill: black)
  } else {
    box(width: cell_size, height: cell_size, stroke: 0.5pt)
  }
  grid(
    columns: (auto, auto),
    column-gutter: 8pt,
    align: (right + top, left + top),
    text(size: 14pt, weight: "bold")[#num.],
    grid(
      columns: range(n).map(_ => cell_size),
      rows: range(n).map(_ => cell_size),
      gutter: 3pt,
      ..cells.map(c => draw_cell(c)),
    ),
  )
}
"""


def _neighbors(cell: tuple[int, int], n: int) -> set[tuple[int, int]]:
    row, col = cell
    return {
        (row + dr, col + dc)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= row + dr < n and 0 <= col + dc < n
    }


def _generate_shape(n: int, min_cells: int, max_cells: int) -> frozenset[tuple[int, int]]:
    target = random.randint(min_cells, max_cells)
    seed = (random.randint(0, n - 1), random.randint(0, n - 1))
    filled: set[tuple[int, int]] = {seed}
    boundary = _neighbors(seed, n)
    while len(filled) < target and boundary:
        cell = random.choice(list(boundary))
        filled.add(cell)
        boundary.discard(cell)
        boundary |= _neighbors(cell, n) - filled
    return frozenset(filled)


@dataclass
class CountingSquaresProblem:
    n: int
    filled: frozenset[tuple[int, int]]

    @property
    def result(self) -> int:
        return len(self.filled)


class CountingSquaresModule(Module):
    _TITLES = {"en": "Count the Squares", "da": "Tæl de farvede felter"}

    @property
    def slug(self) -> str:
        return "counting-squares"

    def title(self, locale: str) -> str:
        return self._TITLES[locale]

    def generate(self, n: int, difficulty: int) -> list[CountingSquaresProblem]:
        if difficulty not in _DIFFICULTY_SETTINGS:
            raise ValueError(f"Difficulty must be 1, 2, or 3, got {difficulty}.")
        grid_n, min_cells, max_cells = _DIFFICULTY_SETTINGS[difficulty]
        return [
            CountingSquaresProblem(n=grid_n, filled=_generate_shape(grid_n, min_cells, max_cells))
            for _ in range(n)
        ]

    def typst_preamble(self) -> str:
        return _PREAMBLE

    def page_source(self, problems: list[CountingSquaresProblem], start_num: int, locale: str) -> str:
        def cells_str(p: CountingSquaresProblem) -> str:
            vals = [
                "1" if (row, col) in p.filled else "0"
                for row in range(p.n)
                for col in range(p.n)
            ]
            return "(" + ", ".join(vals) + ")"

        problem_calls = ",\n    ".join(
            f"problem({start_num + i}, {p.n}, {cells_str(p)})"
            for i, p in enumerate(problems)
        )
        answer_text = "#h(1cm)".join(
            f"{start_num + i}. {p.result}"
            for i, p in enumerate(problems)
        )
        return f"""\
#align(center)[
  #text(size: 24pt, weight: "bold")[{self.title(locale)}]
]

#v(0.8cm)

#align(center)[
  #grid(
    columns: (auto, auto, auto),
    column-gutter: 1cm,
    row-gutter: 2cm,
    {problem_calls}
  )
]

#place(bottom + center)[
  #text(size: 12pt)[{answer_text}]
]"""
