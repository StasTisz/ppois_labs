from __future__ import annotations

from lab2.domain.people.lecturer import Lecturer


class Department:
    def __init__(self, name: str) -> None:
        self.name = name
        self.head: Lecturer | None = None
        self.head_name: str | None = None
        self._teachers: list[Lecturer] = []

    @property
    def staff_count(self) -> int:
        return len(self._teachers)

    def assign_head(self, head: Lecturer | str) -> None:
        if isinstance(head, Lecturer):
            self.head = head
            self.head_name = head.full_name
            if head not in self._teachers:
                self.add_teacher(head)
        else:
            self.head = None
            self.head_name = str(head)

    def add_teacher(self, teacher: Lecturer) -> None:
        if teacher not in self._teachers:
            self._teachers.append(teacher)
            teacher.department = self

    def remove_teacher(self, teacher: Lecturer) -> None:
        if teacher in self._teachers:
            self._teachers.remove(teacher)
            if getattr(teacher, "department", None) == self:
                teacher.department = None
        else:
            name = getattr(teacher, 'full_name', str(teacher))
            raise ValueError(f"Преподаватель {name} не числится на кафедре {self.name}.")
