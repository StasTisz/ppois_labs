from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import ResidentNotFoundException, RoomCapacityExceededException

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class Room:
    DEFAULT_CAPACITY = 4

    def __init__(self, number: str, capacity: int = DEFAULT_CAPACITY) -> None:
        self.number = number
        self.capacity = capacity
        self._residents: list[Student] = []

    @property
    def free_beds(self) -> int:
        return self.capacity - len(self._residents)

    def check_in(self, student: Student) -> None:
        if self.has_resident(student):
            raise ValueError(f"Студент {student.full_name} уже прописан в этой комнате.")
        if self.free_beds <= 0:
            raise RoomCapacityExceededException(f"Блок {self.number} полностью укомплектован.")
        self._residents.append(student)
        student.room = self

    def evict(self, student: Student) -> None:
        if not self.has_resident(student):
            raise ResidentNotFoundException("Студент здесь не проживает.")
        self._residents.remove(student)
        if getattr(student, "room", None) == self:
            student.room = None

    def has_resident(self, student: Student) -> bool:
        return student in self._residents

    @property
    def is_empty(self) -> bool:
        return len(self._residents) == 0

    def evict_all(self) -> None:
        for student in self._residents:
            if getattr(student, "room", None) == self:
                student.room = None
        self._residents.clear()