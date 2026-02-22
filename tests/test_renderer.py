from math_problems.addition import AdditionModule, AdditionProblem
from math_problems.renderer import build_typ_source, render_pdf

FIXED_PROBLEMS = [
    AdditionProblem(3, 4),
    AdditionProblem(7, 2),
    AdditionProblem(1, 8),
    AdditionProblem(5, 6),
    AdditionProblem(9, 3),
    AdditionProblem(2, 7),
    AdditionProblem(4, 5),
    AdditionProblem(8, 1),
    AdditionProblem(6, 9),
]


def test_typ_source_contains_addends():
    source = build_typ_source(AdditionModule(), FIXED_PROBLEMS)
    for p in FIXED_PROBLEMS:
        assert str(p.a) in source
        assert str(p.b) in source


def test_typ_source_contains_answers():
    source = build_typ_source(AdditionModule(), FIXED_PROBLEMS)
    for i, p in enumerate(FIXED_PROBLEMS, start=1):
        assert f"{i}. {p.result}" in source


def test_typ_source_has_upside_down_block():
    source = build_typ_source(AdditionModule(), FIXED_PROBLEMS)
    assert "rotate(180deg)" in source


def test_typ_source_has_problem_numbering():
    source = build_typ_source(AdditionModule(), FIXED_PROBLEMS)
    for i in range(1, 10):
        assert f"problem({i}," in source


def test_render_pdf_returns_valid_pdf():
    pdf_bytes = render_pdf(AdditionModule(), FIXED_PROBLEMS)
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes[:4] == b"%PDF"
