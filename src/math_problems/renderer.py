import os
import tempfile
from typing import Any

import typst

from math_problems.module import Module, _BASE_PREAMBLE


def build_typ_source(pages: list[tuple[Module, list[Any]]]) -> str:
    """Build a Typst source string for a sequence of pages.

    Each entry in pages is a (module, problems) pair. The module's
    typst_preamble() (its #let bindings) is re-emitted before each page so
    different modules can appear on different pages. Problem numbers run
    continuously across pages.
    """
    page_sources = []
    start_num = 1
    for module, problems in pages:
        page_sources.append(
            module.typst_preamble() + "\n" + module.page_source(problems, start_num)
        )
        start_num += len(problems)
    return _BASE_PREAMBLE + "\n" + "\n\n#pagebreak()\n\n".join(page_sources) + "\n"


def render_pdf(pages: list[tuple[Module, list[Any]]]) -> bytes:
    """Compile the problems sheet to PDF and return the bytes."""
    source = build_typ_source(pages)
    with tempfile.NamedTemporaryFile(
        suffix=".typ", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(source)
        tmp_path = f.name
    try:
        return typst.compile(tmp_path)
    finally:
        os.unlink(tmp_path)
