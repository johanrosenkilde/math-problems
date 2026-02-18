import os
import tempfile

import typst


def build_typ_source(problems: list[tuple[int, int]]) -> str:
    """Build a Typst source string for a page of 9 addition problems."""
    problem_calls = ",\n  ".join(
        f"problem({i}, {a}, {b})"
        for i, (a, b) in enumerate(problems, start=1)
    )
    answer_text = "   ".join(
        f"{i}. {a + b}"
        for i, (a, b) in enumerate(problems, start=1)
    )

    return f"""\
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
#set text(font: "New Computer Modern")

#let problem(num, a, b) = {{
  align(center)[
    #text(size: 18pt, weight: "bold")[#num.]
    #v(4pt)
    #box(width: 5.5em)[
      #grid(
        columns: (1.5em, 4em),
        align: (left, right),
        [], [#text(size: 48pt)[#a]],
        [#text(size: 48pt)[+]], [#text(size: 48pt)[#b]],
      )
      #v(2pt)
      #line(length: 5.5em, stroke: 1.5pt)
      #v(2.5em)
    ]
  ]
}}

#grid(
  columns: 3,
  column-gutter: 1cm,
  row-gutter: 0.5cm,
  {problem_calls}
)

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
