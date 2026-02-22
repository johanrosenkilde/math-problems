import os
import tempfile
from typing import Any

import typst

from math_problems.module import Module


def build_typ_source(module: Module, problems: list[Any]) -> str:
    """Build a Typst source string for one or more pages of problems.

    Problems are split into pages of 9. Numbers run continuously across pages.
    """
    pages = [
        module.page_source(problems[i : i + 9], start_num=i + 1)
        for i in range(0, len(problems), 9)
    ]
    return module.typst_preamble() + "\n" + "\n\n#pagebreak()\n\n".join(pages) + "\n"


def render_pdf(module: Module, problems: list[Any]) -> bytes:
    """Compile the problems sheet to PDF and return the bytes."""
    source = build_typ_source(module, problems)
    with tempfile.NamedTemporaryFile(
        suffix=".typ", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(source)
        tmp_path = f.name
    try:
        return typst.compile(tmp_path)
    finally:
        os.unlink(tmp_path)
