from math_problems.problems import generate_addition_problems


def test_returns_nine_problems():
    problems = generate_addition_problems()
    assert len(problems) == 9


def test_values_in_range():
    problems = generate_addition_problems()
    for a, b in problems:
        assert 1 <= a <= 9
        assert 1 <= b <= 9


def test_returns_tuples_of_ints():
    problems = generate_addition_problems()
    for problem in problems:
        assert isinstance(problem, tuple)
        assert len(problem) == 2
        a, b = problem
        assert isinstance(a, int)
        assert isinstance(b, int)


def test_custom_count():
    assert len(generate_addition_problems(n=5)) == 5


def test_custom_range():
    problems = generate_addition_problems(n=50, low=3, high=5)
    for a, b in problems:
        assert 3 <= a <= 5
        assert 3 <= b <= 5
