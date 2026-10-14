from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject


class LabWork:
    DEFAULT_MAX_SCORE = 10.0

    def __init__(
        self,
        title: str,
        max_score: float = DEFAULT_MAX_SCORE,
        lab_number: int = 1,
    ) -> None:
        self.lab_number = lab_number
        self.title = title
        self.max_score = max_score
        self.is_mandatory = True
        self.subject: Subject | None = None

    def make_optional(self) -> None:
        self.is_mandatory = False

    def make_mandatory(self) -> None:
        self.is_mandatory = True

    @property
    def short_info(self) -> str:
        status = "Обязательная" if self.is_mandatory else "Бонусная"
        return (
            f"[{status}] Лаб #{self.lab_number} '{self.title}' (Max: {self.max_score})"
        )

    def update_score_limit(self, new_max: float) -> None:
        if new_max <= 0:
            raise ValueError(
                "Максимальный балл не может быть нулевым или отрицательным."
            )
        self.max_score = new_max

    def __repr__(self) -> str:
        return f"LabWork(number={self.lab_number}, title={self.title!r}, max_score={self.max_score})"
