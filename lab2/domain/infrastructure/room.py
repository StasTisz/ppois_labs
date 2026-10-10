from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class Room:
    """
    Жилая комната (блок) в общежитии.

    Attributes:
        number (str): Номер комнаты.
        capacity (int): Максимальная вместимость (количество спальных мест).
    """
    DEFAULT_CAPACITY = 4

    def __init__(self, number: str, capacity: int = DEFAULT_CAPACITY) -> None:
        self.number = number
        self.capacity = capacity
        self._residents: list[Student] = []

    @property
    def free_beds(self) -> int:
        """Агрегация: вычисляет количество свободных мест в комнате."""
        return self.capacity - len(self._residents)

    def check_in(self, student: Student) -> None:
        """
        Заселяет студента в комнату.

        Args:
            student (Student): Студент для заселения.

        Raises:
            ValueError: Если комната полностью укомплектована или студент уже заселен.
        """
        if self.free_beds <= 0:
            raise ValueError(f"Блок {self.number} полностью укомплектован.")
        if self.has_resident(student):
            raise ValueError(f"Студент {student.full_name} уже прописан в этой комнате.")
        self._residents.append(student)
        student.room = self

    def evict(self, student: Student) -> None:
        """
        Выселяет студента из комнаты.

        Args:
            student (Student): Студент для выселения.

        Raises:
            ValueError: Если студент не проживает в этой комнате.
        """
        if not self.has_resident(student):
            raise ValueError("Студент здесь не проживает.")
        self._residents.remove(student)
        if getattr(student, "room", None) == self:
            student.room = None

    def has_resident(self, student: Student) -> bool:
        """
        Проверяет, проживает ли конкретный студент в этой комнате.

        Args:
            student (Student): Искомый студент.

        Returns:
            bool: True, если студент числится в комнате, иначе False.
        """
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
