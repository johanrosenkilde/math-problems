import random
from dataclasses import dataclass

from math_problems.module import Module, arithmetic_preamble, build_page_layout


_DIFFICULTY_RANGES: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {
    1: ((2, 9),   (2, 9)),
    2: ((2, 9),   (11, 20)),
    3: ((11, 25), (11, 25)),
}

_PREAMBLE = arithmetic_preamble("\u00f7")


@dataclass
class DivisionProblem:
    divisor: int
    result: int

    @property
    def dividend(self) -> int:
        return self.divisor * self.result


class DivisionModule(Module):
    _TITLES = {"en": "Division", "da": "Division"}

    @property
    def slug(self) -> str:
        return "division"

    def title(self, locale: str) -> str:
        return self._TITLES[locale]

    def _make(self, divisor_range: tuple[int, int], result_range: tuple[int, int]) -> DivisionProblem:
        return DivisionProblem(random.randint(*divisor_range), random.randint(*result_range))

    def generate(self, n: int, difficulty: float) -> list[DivisionProblem]:
        if difficulty in (1.5, 2.5):
            lo, hi = _DIFFICULTY_RANGES[int(difficulty - 0.5)], _DIFFICULTY_RANGES[int(difficulty + 0.5)]
            n_easy = min(6, n)
            return [self._make(*lo) for _ in range(n_easy)] + [self._make(*hi) for _ in range(n - n_easy)]
        if difficulty not in _DIFFICULTY_RANGES:
            raise ValueError(f"Difficulty must be 1, 1.5, 2, 2.5, or 3, got {difficulty}.")
        return [self._make(*_DIFFICULTY_RANGES[difficulty]) for _ in range(n)]

    def typst_preamble(self) -> str:
        return _PREAMBLE

    def page_source(self, problems: list[DivisionProblem], start_num: int, locale: str) -> str:
        problem_calls = ",\n    ".join(
            f"problem({start_num + i}, {p.dividend}, {p.divisor})"
            for i, p in enumerate(problems)
        )
        return build_page_layout(
            self.title(locale), problem_calls,
            [(start_num + i, p.result) for i, p in enumerate(problems)],
        )
