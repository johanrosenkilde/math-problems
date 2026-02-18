import pytest

from math_problems.problems import generate_addition_problems
from math_problems.renderer import build_typ_source, render_pdf

FIXED_PROBLEMS = [(3, 4), (7, 2), (1, 8), (5, 6), (9, 3), (2, 7), (4, 5), (8, 1), (6, 9)]


def test_typ_source_contains_addends():
    source = build_typ_source(FIXED_PROBLEMS)
    for a, b in FIXED_PROBLEMS:
        assert str(a) in source
        assert str(b) in source


def test_typ_source_contains_answers():
    source = build_typ_source(FIXED_PROBLEMS)
    for i, (a, b) in enumerate(FIXED_PROBLEMS, start=1):
        assert f"{i}. {a + b}" in source


def test_typ_source_has_upside_down_block():
    source = build_typ_source(FIXED_PROBLEMS)
    assert "rotate(180deg)" in source


def test_typ_source_has_problem_numbering():
    source = build_typ_source(FIXED_PROBLEMS)
    for i in range(1, 10):
        assert f"problem({i}," in source


def test_render_pdf_returns_valid_pdf():
    pdf_bytes = render_pdf(FIXED_PROBLEMS)
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes[:4] == b"%PDF"
