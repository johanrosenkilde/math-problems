import pytest

from math_problems.grocery_list import (
    GroceryListModule,
    GroceryListProblem,
    _DIFFICULTY_SETTINGS,
    _SYMBOLS,
)


def test_problem_result():
    legend = {"🍌": 5, "🍎": 3}
    assert GroceryListProblem([("🍌", 3), ("🍎", 2)], legend).result == 21
    assert GroceryListProblem([("🍎", 1)], legend).result == 3


def test_problem_result_three_symbols():
    legend = {"🍌": 10, "🍎": 3, "🍒": 5}
    assert GroceryListProblem([("🍌", 2), ("🍎", 4), ("🍒", 1)], legend).result == 37


def test_generate_returns_nine_problems():
    assert len(GroceryListModule().generate(n=9, difficulty=1)) == 9


def test_generate_custom_count():
    assert len(GroceryListModule().generate(n=5, difficulty=1)) == 5


def test_generate_returns_correct_type():
    for problem in GroceryListModule().generate(n=9, difficulty=1):
        assert isinstance(problem, GroceryListProblem)
        for emoji, count in problem.items:
            assert emoji in _SYMBOLS
            assert isinstance(count, int)


def test_page_shares_legend():
    problems = GroceryListModule().generate(n=9, difficulty=2)
    first_legend = problems[0].legend
    for p in problems:
        assert p.legend is first_legend


def test_problem_items_are_subset_of_legend():
    for difficulty in _DIFFICULTY_SETTINGS:
        problems = GroceryListModule().generate(n=20, difficulty=difficulty)
        for p in problems:
            for emoji, _ in p.items:
                assert emoji in p.legend


@pytest.mark.parametrize("difficulty", _DIFFICULTY_SETTINGS)
def test_difficulty_range(difficulty):
    page_sym_count, (p_lo, p_hi), (v_lo, v_hi), (c_lo, c_hi) = _DIFFICULTY_SETTINGS[difficulty]
    problems = GroceryListModule().generate(n=50, difficulty=difficulty)
    assert len(problems[0].legend) == page_sym_count
    for p in problems:
        assert p_lo <= len(p.items) <= p_hi
        for _, count in p.items:
            assert c_lo <= count <= c_hi
    for value in problems[0].legend.values():
        assert v_lo <= value <= v_hi


def test_symbols_are_distinct_within_problem():
    problems = GroceryListModule().generate(n=50, difficulty=3)
    for p in problems:
        emojis = [emoji for emoji, _ in p.items]
        assert len(emojis) == len(set(emojis))


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        GroceryListModule().generate(n=9, difficulty=4)
