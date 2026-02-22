import os
import tempfile

import typst


def build_typ_source(problems: list[tuple[int, int]]) -> str:
    """Build a Typst source string for a page of 9 addition problems."""
    problem_calls = ",\n    ".join(
        f"problem({i}, {a}, {b})"
        for i, (a, b) in enumerate(problems, start=1)
    )
    answer_text = "#h(1.2cm)".join(
        f"{i}. {a + b}"
        for i, (a, b) in enumerate(problems, start=1)
    )

    return f"""\
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
#set text(font: "New Computer Modern")

#let problem(num, a, b) = {{
  grid(
    columns: (auto, 1.8cm),
    column-gutter: 3pt,
    align: (right + top, left + top),
    text(size: 14pt, weight: "bold")[#num.],
    [
      #grid(
        columns: (0.6cm, 1.2cm),
        column-gutter: 0pt,
        row-gutter: 14pt,
        align: (left, right),
        [], [#text(size: 40pt)[#a]],
        [#text(size: 40pt)[+]], [#text(size: 40pt)[#b]],
      )
      #v(2pt)
      #line(length: 100%, stroke: 1.5pt)
      #v(2cm)
    ]
  )
}}

#align(center)[
  #text(size: 24pt, weight: "bold")[Addition]
]

#v(0.8cm)

#align(center)[
  #grid(
    columns: (auto, auto, auto),
    column-gutter: 2.5cm,
    row-gutter: 1.2cm,
    {problem_calls}
  )
]

#v(1fr)

#align(center)[
  #rotate(180deg)[
    #text(size: 12pt)[{answer_text}]
  ]
]
"""


def render_pdf(problems: list[tuple[int, int]]) -> bytes:
    """Compile the addition problems sheet to PDF and return the bytes."""
    source = build_typ_source(problems)
    with tempfile.NamedTemporaryFile(
        suffix=".typ", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(source)
        tmp_path = f.name
    try:
        return typst.compile(tmp_path)
    finally:
        os.unlink(tmp_path)
