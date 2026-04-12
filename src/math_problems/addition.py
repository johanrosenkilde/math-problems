import random
from dataclasses import dataclass

from math_problems.module import Module, arithmetic_preamble, build_page_layout


_DIFFICULTY_RANGES: dict[int, tuple[int, int]] = {
    1: (1, 9),
    2: (10, 99),
    3: (100, 499),
}

_PREAMBLE = arithmetic_preamble("+")


@dataclass
class AdditionProblem:
    a: int
    b: int

    @property
    def result(self) -> int:
        return self.a + self.b


class AdditionModule(Module):
    _TITLES = {"en": "Addition", "da": "Addition"}

    @property
    def slug(self) -> str:
        return "addition"

    def title(self, locale: str) -> str:
        return self._TITLES[locale]

    def _make(self, low: int, high: int) -> AdditionProblem:
        return AdditionProblem(random.randint(low, high), random.randint(low, high))

    def generate(self, n: int, difficulty: float) -> list[AdditionProblem]:
        if difficulty in (1.5, 2.5):
            lo, hi = _DIFFICULTY_RANGES[int(difficulty - 0.5)], _DIFFICULTY_RANGES[int(difficulty + 0.5)]
            n_easy = min(6, n)
            return [self._make(*lo) for _ in range(n_easy)] + [self._make(*hi) for _ in range(n - n_easy)]
        if difficulty not in _DIFFICULTY_RANGES:
            raise ValueError(f"Difficulty must be 1, 1.5, 2, 2.5, or 3, got {difficulty}.")
        return [self._make(*_DIFFICULTY_RANGES[difficulty]) for _ in range(n)]

    def typst_preamble(self) -> str:
        return _PREAMBLE

    def page_source(self, problems: list[AdditionProblem], start_num: int, locale: str) -> str:
        problem_calls = ",\n    ".join(
            f"problem({start_num + i}, {p.a}, {p.b})"
            for i, p in enumerate(problems)
        )
        return build_page_layout(
            self.title(locale), problem_calls,
            [(start_num + i, p.result) for i, p in enumerate(problems)],
        )
