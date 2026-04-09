import random
from dataclasses import dataclass

from math_problems.module import Module


_SYMBOLS = [
    # Fruit & veg
    "🍌", "🍎", "🍒", "🍇", "🍊", "🍋", "🍐", "🍓", "🥕", "🌽",
    "🍉", "🥒", "🫑", "🍆", "🥦", "🧅",
    # Bakery & dairy
    "🥐", "🧁", "🍩", "🥖", "🥚", "🧀", "🥛", "🍞",
    # Other grocery
    "🍬", "🍫", "🧃", "🥜", "🍿", "🍯", "🫙",
]

_DIFFICULTY_SETTINGS: dict[int, tuple[int, tuple[int, int], tuple[int, int], tuple[int, int]]] = {
    #  (page_symbols, per_problem_range, value_range, count_range)
    1: (3, (1, 2), (1, 5), (1, 3)),
    2: (4, (2, 3), (2, 9), (2, 5)),
    3: (5, (2, 4), (3, 12), (2, 4)),
}

_PREAMBLE = """\
#set text(font: ("New Computer Modern", "Apple Color Emoji"))
"""


@dataclass
class GroceryListProblem:
    items: list[tuple[str, int]]  # (emoji, count) — symbols used in this problem
    legend: dict[str, int]  # full page legend: emoji -> value

    @property
    def result(self) -> int:
        return sum(self.legend[emoji] * count for emoji, count in self.items)


class GroceryListModule(Module):
    _TITLES = {"en": "Grocery List", "da": "Indkøbsliste"}

    @property
    def slug(self) -> str:
        return "grocery-list"

    def title(self, locale: str) -> str:
        return self._TITLES[locale]

    def generate(self, n: int, difficulty: int) -> list[GroceryListProblem]:
        if difficulty not in _DIFFICULTY_SETTINGS:
            raise ValueError(f"Difficulty must be 1, 2, or 3, got {difficulty}.")
        page_sym_count, per_problem_range, val_range, count_range = _DIFFICULTY_SETTINGS[difficulty]
        chosen = random.sample(_SYMBOLS, page_sym_count)
        legend = {emoji: random.randint(*val_range) for emoji in chosen}
        problems = []
        for _ in range(n):
            k = random.randint(*per_problem_range)
            used = random.sample(chosen, k)
            items = [(emoji, random.randint(*count_range)) for emoji in used]
            random.shuffle(items)
            problems.append(GroceryListProblem(items=items, legend=legend))
        return problems

    def typst_preamble(self) -> str:
        return _PREAMBLE

    def page_source(self, problems: list[GroceryListProblem], start_num: int, locale: str) -> str:
        legend = problems[0].legend
        legend_parts = [f"{emoji} = {value}" for emoji, value in legend.items()]
        legend_str = " #h(1.5cm) ".join(legend_parts)

        problem_calls = ",\n    ".join(
            self._problem_call(start_num + i, p)
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

#v(0.3cm)

#align(center)[
  #text(size: 20pt)[{legend_str}]
]

#v(0.5cm)

#align(center)[
  #grid(
    columns: (auto, auto, auto),
    column-gutter: 1.5cm,
    row-gutter: 1.2cm,
    {problem_calls}
  )
]

#place(bottom + center)[
  #text(size: 12pt)[{answer_text}]
]"""

    def _problem_call(self, num: int, p: GroceryListProblem) -> str:
        rows = []
        for emoji, count in p.items:
            row_content = " ".join([emoji] * count)
            rows.append(f"text(size: 24pt)[{row_content}]")
        stack_items = ",\n      ".join(rows)
        return f"""context {{
  let inner = stack(
    dir: ttb,
    spacing: 8pt,
    {stack_items},
  )
  let w = measure(inner).width
  grid(
    columns: (auto, auto),
    column-gutter: 8pt,
    align: (right + top, left + top),
    text(size: 14pt, weight: "bold")[{num}.],
    {{
      v(10pt)
      inner
      v(2pt)
      line(length: w, stroke: 1.5pt)
      v(30pt)
      line(length: w, stroke: 1.5pt)
      v(-8pt)
      line(length: w, stroke: 1.5pt)
      v(1cm)
    }}
  )
}}"""
