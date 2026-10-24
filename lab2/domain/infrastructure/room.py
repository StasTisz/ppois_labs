"""Модуль жилой комнаты студенческого общежития."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import (
    ResidentNotFoundException,
    RoomCapacityExceededException,
)

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class Room:
    """Жилая комната (блок) в общежитии."""

    DEFAULT_CAPACITY = 4

    def __init__(self, number: str, capacity: int = DEFAULT_CAPACITY) -> None:
        """Инициализирует экземпляр класса Room."""
        self.number = number
        self.capacity = capacity
        self._residents: list[Student] = []

    @property
    def residents(self) -> list[Student]:
        """Возвращает значение атрибута residents."""
        return list(self._residents)

    @property
    def free_beds(self) -> int:
        """Агрегация: вычисляет количество свободных мест в комнате."""
        return self.capacity - len(self._residents)

    def check_in(self, student: Student) -> None:
        """Заселяет студента в комнату."""
        if self.has_resident(student):
            raise ValueError(
                f"Студент {student.full_name} уже прописан в этой комнате."
            )
        if self.free_beds <= 0:
            raise RoomCapacityExceededException(
                f"Блок {self.number} полностью укомплектован."
            )
        self._residents.append(student)
        student.room = self

    def evict(self, student: Student) -> None:
        """Выселяет студента из комнаты."""
        if not self.has_resident(student):
            raise ResidentNotFoundException("Студент здесь не проживает.")
        self._residents.remove(student)
        if getattr(student, "room", None) == self:
            student.room = None

    def has_resident(self, student: Student) -> bool:
        """Проверяет, проживает ли конкретный студент в этой комнате."""
        return student in self._residents

    @property
    def is_empty(self) -> bool:
        """Проверяет, пустует ли комната."""
        return len(self._residents) == 0

    def evict_all(self) -> None:
        """Массово выселяет всех проживающих (например, на время летнего ремонта)."""
        for student in self._residents:
            if getattr(student, "room", None) == self:
                student.room = None
        self._residents.clear()

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Room(number={self.number!r}, capacity={self.capacity}, residents={len(self._residents)})"
