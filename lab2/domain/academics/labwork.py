"""Модуль учебной лабораторной работы курса."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject


class LabWork:
    """Учебная лабораторная работа."""

    DEFAULT_MAX_SCORE = 10.0

    def __init__(
        self,
        title: str,
        max_score: float = DEFAULT_MAX_SCORE,
        lab_number: int = 1,
    ) -> None:
        """Инициализирует экземпляр класса LabWork."""
        self.lab_number = lab_number
        self.title = title
        self.max_score = max_score
        self.is_mandatory = True
        self.subject: Subject | None = None

    def make_optional(self) -> None:
        """Делает лабораторную работу необязательной (бонусной)."""
        self.is_mandatory = False

    def make_mandatory(self) -> None:
        """Делает лабораторную работу обязательной для сдачи."""
        self.is_mandatory = True

    @property
    def short_info(self) -> str:
        """Агрегация: возвращает краткую информацию о статусе и баллах."""
        status = "Обязательная" if self.is_mandatory else "Бонусная"
        return (
            f"[{status}] Лаб #{self.lab_number} '{self.title}' (Max: {self.max_score})"
        )

    def update_score_limit(self, new_max: float) -> None:
        """Корректирует максимальный балл за лабораторную работу."""
        if new_max <= 0:
            raise ValueError(
                "Максимальный балл не может быть нулевым или отрицательным."
            )
        self.max_score = new_max

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"LabWork(number={self.lab_number}, title={self.title!r}, max_score={self.max_score})"
