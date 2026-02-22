from abc import ABC, abstractmethod
from typing import Any


class Module(ABC):
    @property
    @abstractmethod
    def title(self) -> str:
        """Display name used as the page headline."""

    @abstractmethod
    def generate(self, n: int, difficulty: int) -> list[Any]:
        """Generate n problems at the given difficulty level."""

    @abstractmethod
    def typst_preamble(self) -> str:
        """Typst source: page/text setup + let-bindings for this module."""

    @abstractmethod
    def page_source(self, problems: list[Any], start_num: int) -> str:
        """Typst markup for a single page of up to 9 problems."""
