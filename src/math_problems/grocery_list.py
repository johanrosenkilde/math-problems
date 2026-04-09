import random
from dataclasses import dataclass

from math_problems.module import Module


_INGREDIENTS = [
    # Fruit & veg
    "🍌", "🍎", "🍒", "🍇", "🍊", "🍋", "🍐", "🍓", "🥕", "🌽",
    "🍉", "🥒", "🫑", "🍆", "🥦", "🧅",
    # Bakery & dairy
    "🥐", "🧁", "🍩", "🥖", "🥚", "🧀", "🥛", "🍞",
    # Other grocery
    "🍬", "🍫", "🧃", "🥜", "🍿", "🍯", "🫙",
]

_DIFFICULTY_SETTINGS: dict[int, tuple[int, tuple[int, int], tuple[int, int], tuple[int, int]]] = {
    #  (page_ingredients, per_problem_range, value_range, count_range)
    1: (3, (2, 2), (1, 5), (1, 3)),
    2: (4, (2, 3), (2, 9), (2, 5)),
    3: (5, (3, 3), (3, 12), (2, 4)),
}

_PREAMBLE = """\
#set text(font: ("New Computer Modern", "Apple Color Emoji"))
"""


@dataclass
class GroceryListProblem:
    items: list[tuple[str, int]]  # (emoji, count) — ingredients in this problem
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
        n_ingredients, per_problem_range, val_range, count_range = _DIFFICULTY_SETTINGS[difficulty]
        chosen = random.sample(_INGREDIENTS, n_ingredients)
        values = random.sample(range(val_range[0], val_range[1] + 1), n_ingredients)
        legend = dict(zip(chosen, values))
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
        legend_gap = "#h(1fr)" if len(legend) > 3 else "#h(1.5cm)"
        legend_str = f" {legend_gap} ".join(legend_parts)

        problem_calls = ",\n    ".join(
            self._problem_call(start_num + i, p)
            for i, p in enumerate(problems)
        )
        answer_text = "#h(1cm)".join(
            f"{start_num + i}. {p.result}"
            for i, p in enumerate(problems)
        )
        # A4 content area: 297mm − 2×25mm margins = 247mm.
        # Reserve header (~50mm, includes title + legend + paragraph spacing)
        # and answer line (~10mm); the rest is split into 3 equal rows
        # with 0.4cm gutters between them.
        row_h_mm = (247 - 50 - 10 - 2 * 4) // 3  # = 59mm

        return f"""\
#align(center)[
  #text(size: 24pt, weight: "bold")[{self.title(locale)}]
]

#v(0.3cm)

#align(center)[
  #text(size: 20pt)[{legend_str}]
]

#v(0.5cm)

#grid(
    columns: (1fr, 1fr, 1fr),
    rows: ({row_h_mm}mm, {row_h_mm}mm, {row_h_mm}mm),
    column-gutter: 0.8cm,
    row-gutter: 0.4cm,
    align: (left + top),
    {problem_calls}
  )

#v(1fr)

#align(center)[
  #text(size: 12pt)[{answer_text}]
]"""

    def _problem_call(self, num: int, p: GroceryListProblem) -> str:
        # Dynamic font size and spacing so each problem fills its grid cell.
        # Font and total icon-stack height are each snapped to one of 3
        # buckets so that answer lines land at consistent positions.
        line_h = 2.0    # line-height factor for emoji (colour emoji are tall)
        avail_w = 90    # usable width for one icon row in pt

        # Count visual rows and widest row (wrapping rows with > 5 icons)
        visual_rows = 0
        max_per_row = 0
        for _, count in p.items:
            if count <= 5:
                visual_rows += 1
                max_per_row = max(max_per_row, count)
            else:
                visual_rows += (count + 2) // 3
                max_per_row = max(max_per_row, 3)

        # Raw font size from width and height constraints
        raw_fs = min(avail_w / max(max_per_row, 1),
                     130 / (visual_rows * line_h), 36)

        # Snap to one of 3 font-size buckets
        if raw_fs >= 26:
            fs = 30
        elif raw_fs >= 19:
            fs = 21
        else:
            fs = 18

        # Target total icon-stack height (3 buckets → answer lines align)
        if visual_rows >= 3 or fs == 30:
            icon_target = 130
        elif fs == 21:
            icon_target = 90
        else:
            icon_target = 75

        if visual_rows > 1:
            used = visual_rows * fs * line_h
            spacing = (icon_target - used) / (visual_rows - 1)
            spacing = max(spacing, -fs * 0.3)  # limit overlap
        else:
            spacing = 0

        # Build emoji rows
        rows = []
        for emoji, count in p.items:
            if count <= 5:
                row_content = " ".join([emoji] * count)
                rows.append(f"text(size: {fs}pt)[{row_content}]")
            else:
                for i in range(0, count, 3):
                    chunk = min(3, count - i)
                    row_content = " ".join([emoji] * chunk)
                    rows.append(f"text(size: {fs}pt)[{row_content}]")

        stack_items = ",\n      ".join(rows)
        return f"""context {{
  let inner = stack(
    dir: ttb,
    spacing: {round(spacing, 1)}pt,
    {stack_items},
  )
  let w = measure(inner).width
  grid(
    columns: (auto, auto),
    column-gutter: 8pt,
    align: (right + top, left + top),
    text(size: 14pt, weight: "bold")[{num}.],
    {{
      v(6pt)
      inner
      v(2pt)
      line(length: w, stroke: 1.5pt)
      v(20pt)
      line(length: w, stroke: 1.5pt)
      v(-8pt)
      line(length: w, stroke: 1.5pt)
      v(0.5cm)
    }}
  )
}}"""
