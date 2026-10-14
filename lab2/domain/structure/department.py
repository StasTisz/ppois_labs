from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.people.lecturer import Lecturer


class Department:
    def __init__(self, name: str) -> None:
        self.name = name
        self._head: Lecturer | None = None
        self._head_str_fallback: str | None = None
        self._teachers: list[Lecturer] = []

    @property
    def head(self) -> Lecturer | None:
        return self._head

    @property
    def head_name(self) -> str | None:
        if self._head:
            return self._head.full_name
        return self._head_str_fallback

    @property
    def staff_count(self) -> int:
        return len(self._teachers)

    @property
    def teachers(self) -> list[Lecturer]:
        return list(self._teachers)

    def has_teacher(self, teacher: Lecturer) -> bool:
        return teacher in self._teachers

    def assign_head(self, head: Lecturer | str) -> None:
        if isinstance(head, str):
            self._head = None
            self._head_str_fallback = head
        else:
            self._head = head
            self._head_str_fallback = head.full_name
            if not self.has_teacher(head):
                self.add_teacher(head)

    def add_teacher(self, teacher: Lecturer) -> None:
        if not self.has_teacher(teacher):
            self._teachers.append(teacher)
            teacher.department = self

    def remove_teacher(self, teacher: Lecturer) -> None:
        if self.has_teacher(teacher):
            self._teachers.remove(teacher)
            if getattr(teacher, "department", None) == self:
                teacher.department = None
            if self._head == teacher:
                self._head = None
        else:
            raise ValueError(
                f"Преподаватель {teacher.full_name} не числится на кафедре {self.name}."
            )

    def __repr__(self) -> str:
        head_str = self.head_name or "None"
        return f"Department(name={self.name!r}, head={head_str!r}, staff={self.staff_count})"
