import pytest

from math_problems.counting_squares import (
    CountingSquaresModule,
    CountingSquaresProblem,
    _DIFFICULTY_SETTINGS,
    _generate_shape,
)


def _is_contiguous(filled: frozenset[tuple[int, int]]) -> bool:
    if not filled:
        return True
    cells = set(filled)
    start = next(iter(cells))
    visited = {start}
    queue = [start]
    while queue:
        row, col = queue.pop()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (row + dr, col + dc)
            if neighbor in cells and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited) == len(cells)


def test_result_is_len_filled():
    filled = frozenset({(0, 0), (0, 1), (1, 0)})
    p = CountingSquaresProblem(n=5, filled=filled)
    assert p.result == 3
    assert p.result == len(filled)


def test_shape_is_contiguous():
    for n, min_cells, max_cells in _DIFFICULTY_SETTINGS.values():
        for _ in range(10):
            filled = _generate_shape(n, min_cells, max_cells)
            assert _is_contiguous(filled)


def test_difficulty_settings():
    assert _DIFFICULTY_SETTINGS[1] == (5,  6, 12)
    assert _DIFFICULTY_SETTINGS[2] == (6, 10, 18)
    assert _DIFFICULTY_SETTINGS[3] == (10, 20, 40)


def test_difficulty_grid_size():
    for difficulty, (expected_n, *_) in _DIFFICULTY_SETTINGS.items():
        problems = CountingSquaresModule().generate(n=5, difficulty=difficulty)
        for p in problems:
            assert p.n == expected_n


def test_difficulty_filled_cells_in_bounds():
    for difficulty, (expected_n, *_) in _DIFFICULTY_SETTINGS.items():
        problems = CountingSquaresModule().generate(n=10, difficulty=difficulty)
        for p in problems:
            for row, col in p.filled:
                assert 0 <= row < expected_n
                assert 0 <= col < expected_n


def test_generate_returns_correct_count():
    assert len(CountingSquaresModule().generate(n=9, difficulty=1)) == 9
    assert len(CountingSquaresModule().generate(n=5, difficulty=2)) == 5


def test_generate_returns_correct_type():
    for p in CountingSquaresModule().generate(n=9, difficulty=1):
        assert isinstance(p, CountingSquaresProblem)
        assert isinstance(p.filled, frozenset)
        assert isinstance(p.n, int)


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        CountingSquaresModule().generate(n=9, difficulty=4)


def test_filled_cells_count_in_range():
    for difficulty, (_, min_cells, max_cells) in _DIFFICULTY_SETTINGS.items():
        for p in CountingSquaresModule().generate(n=10, difficulty=difficulty):
            assert min_cells <= p.result <= max_cells
