import random
from dataclasses import dataclass

from math_problems.module import Module


_DIFFICULTY_SETTINGS: dict[int, tuple[int, int]] = {
    1: (5, 2),
    2: (6, 3),
    3: (8, 5),
}

_PREAMBLE = """\
#let problem(num, n, cells) = {
  let cell_size = if n <= 5 { 0.8cm } else if n == 6 { 0.7cm } else { 0.6cm }
  grid(
    columns: (auto, auto),
    column-gutter: 8pt,
    align: (right + top, left + top),
    text(size: 14pt, weight: "bold")[#num.],
    table(
      columns: range(n).map(_ => cell_size),
      rows: range(n).map(_ => cell_size),
      stroke: 0.5pt,
      ..cells.map(c => if c == 1 { table.cell(fill: black)[] } else { [] }),
    ),
  )
}
"""


def _generate_shape(n: int, r: int) -> frozenset[tuple[int, int]]:
    max_dim = n // 2 + 1

    def random_rect_at(anchor_row: int, anchor_col: int) -> set[tuple[int, int]]:
        h = random.randint(2, max_dim)
        w = random.randint(2, max_dim)
        row_start = random.randint(max(0, anchor_row - h + 1), min(n - h, anchor_row))
        col_start = random.randint(max(0, anchor_col - w + 1), min(n - w, anchor_col))
        return {(row_start + dr, col_start + dc) for dr in range(h) for dc in range(w)}

    h = random.randint(2, max_dim)
    w = random.randint(2, max_dim)
    row = random.randint(0, n - h)
    col = random.randint(0, n - w)
    filled: set[tuple[int, int]] = {(row + dr, col + dc) for dr in range(h) for dc in range(w)}

    for _ in range(r - 1):
        anchor_row, anchor_col = random.choice(list(filled))
        filled |= random_rect_at(anchor_row, anchor_col)

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
        grid_n, r = _DIFFICULTY_SETTINGS[difficulty]
        return [
            CountingSquaresProblem(n=grid_n, filled=_generate_shape(grid_n, r))
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
    row-gutter: 1cm,
    {problem_calls}
  )
]

#place(bottom + center)[
  #text(size: 12pt)[{answer_text}]
]"""
