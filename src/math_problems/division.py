import random
from dataclasses import dataclass

from math_problems.module import Module


_DIFFICULTY_RANGES: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {
    1: ((2, 9),   (2, 9)),
    2: ((2, 9),   (11, 20)),
    3: ((11, 25), (11, 25)),
}

_PREAMBLE = """\
#let problem(num, a, b) = context {
  let inner = grid(
    columns: (auto, auto),
    column-gutter: 0pt,
    row-gutter: 18pt,
    align: (left, right),
    [], text(size: 40pt)[#a],
    text(size: 40pt)[÷], text(size: 40pt)[#b],
  )
  let w = measure(inner).width
  grid(
    columns: (auto, auto),
    column-gutter: 8pt,
    align: (right + top, left + top),
    text(size: 14pt, weight: "bold")[#num.],
    {
      v(10pt)
      inner
      v(2pt)
      line(length: w, stroke: 1.5pt)
      v(30pt)
      line(length: w, stroke: 1.5pt)
      v(-8pt)
      line(length: w, stroke: 1.5pt)
      v(1cm)
    }
  )
}
"""


@dataclass
class DivisionProblem:
    divisor: int
    result: int

    @property
    def dividend(self) -> int:
        return self.divisor * self.result


class DivisionModule(Module):
    @property
    def slug(self) -> str:
        return "division"

    @property
    def title(self) -> str:
        return "Division"

    def generate(self, n: int, difficulty: int) -> list[DivisionProblem]:
        if difficulty not in _DIFFICULTY_RANGES:
            raise ValueError(f"Difficulty must be 1, 2, or 3, got {difficulty}.")
        divisor_range, result_range = _DIFFICULTY_RANGES[difficulty]
        return [
            DivisionProblem(random.randint(*divisor_range), random.randint(*result_range))
            for _ in range(n)
        ]

    def typst_preamble(self) -> str:
        return _PREAMBLE

    def page_source(self, problems: list[DivisionProblem], start_num: int) -> str:
        problem_calls = ",\n    ".join(
            f"problem({start_num + i}, {p.dividend}, {p.divisor})"
            for i, p in enumerate(problems)
        )
        answer_text = "#h(1cm)".join(
            f"{start_num + i}. {p.result}"
            for i, p in enumerate(problems)
        )
        return f"""\
#align(center)[
  #text(size: 24pt, weight: "bold")[{self.title}]
]

#v(0.8cm)

#align(center)[
  #grid(
    columns: (auto, auto, auto),
    column-gutter: 2.5cm,
    row-gutter: 1.6cm,
    {problem_calls}
  )
]

#place(bottom + center)[
  #text(size: 12pt)[{answer_text}]
]"""
