import random
from dataclasses import dataclass

from math_problems.module import Module


_DIFFICULTY_RANGES: dict[int, tuple[int, int]] = {
    1: (1, 9),
    2: (10, 99),
    3: (100, 499),
}

_PREAMBLE = """\
#let problem(num, a, b) = context {
  let inner = grid(
    columns: (auto, auto),
    column-gutter: 0pt,
    row-gutter: 18pt,
    align: (left, right),
    [], text(size: 40pt)[#a],
    text(size: 40pt)[+], text(size: 40pt)[#b],
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
class AdditionProblem:
    a: int
    b: int

    @property
    def result(self) -> int:
        return self.a + self.b


class AdditionModule(Module):
    @property
    def title(self) -> str:
        return "Addition"

    def generate(self, n: int, difficulty: int) -> list[AdditionProblem]:
        if difficulty not in _DIFFICULTY_RANGES:
            raise ValueError(f"Difficulty must be 1, 2, or 3, got {difficulty}.")
        low, high = _DIFFICULTY_RANGES[difficulty]
        return [
            AdditionProblem(random.randint(low, high), random.randint(low, high))
            for _ in range(n)
        ]

    def typst_preamble(self) -> str:
        return _PREAMBLE

    def page_source(self, problems: list[AdditionProblem], start_num: int) -> str:
        problem_calls = ",\n    ".join(
            f"problem({start_num + i}, {p.a}, {p.b})"
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
  #rotate(180deg)[
    #text(size: 12pt)[{answer_text}]
  ]
]"""
