import os
import tempfile

import typst


_PREAMBLE = """\
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
#set text(font: "New Computer Modern")

#let problem(num, a, b) = {
  grid(
    columns: (auto, 2cm),
    column-gutter: 8pt,
    align: (right + top, left + top),
    text(size: 14pt, weight: "bold")[#num.],
    [
      #v(10pt)
      #grid(
        columns: (0.8cm, 1.2cm),
        column-gutter: 0pt,
        row-gutter: 18pt,
        align: (left, right),
        [], [#text(size: 40pt)[#a]],
        [#text(size: 40pt)[+]], [#text(size: 40pt)[#b]],
      )
      #v(2pt)
      #line(length: 100%, stroke: 1.5pt)
      #v(30pt)
      #line(length: 100%, stroke: 1.5pt)
      #v(-8pt)
      #line(length: 100%, stroke: 1.5pt)
      #v(1cm)
    ]
  )
}
"""


def _page_source(problems: list[tuple[int, int]], start_num: int) -> str:
    """Build Typst content for a single page, with problem numbers starting at start_num."""
    problem_calls = ",\n    ".join(
        f"problem({start_num + i}, {a}, {b})"
        for i, (a, b) in enumerate(problems)
    )
    answer_text = "#h(1cm)".join(
        f"{start_num + i}. {a + b}"
        for i, (a, b) in enumerate(problems)
    )
    return f"""\
#align(center)[
  #text(size: 24pt, weight: "bold")[Addition]
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


def build_typ_source(problems: list[tuple[int, int]]) -> str:
    """Build a Typst source string for one or more pages of addition problems.

    Problems are split into pages of 9. Numbers run continuously across pages.
    """
    pages = [
        _page_source(problems[i : i + 9], start_num=i + 1)
        for i in range(0, len(problems), 9)
    ]
    return _PREAMBLE + "\n" + "\n\n#pagebreak()\n\n".join(pages) + "\n"


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
