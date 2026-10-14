from __future__ import annotations

from typing import TYPE_CHECKING, Any

from lab2.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.structure.department import Department


class Lecturer(Employee):
    DEFAULT_DEGREE = "Без степени"
    DEFAULT_POSITION = "Преподаватель"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = DEFAULT_DEGREE,
        position: str = DEFAULT_POSITION,
        passport_number: str = "",
    ) -> None:
        super().__init__(
            first_name,
            last_name,
            middle_name,
            position=position,
            passport_number=passport_number,
        )
        self.degree = degree
        self.department: Department | None = None
        self._subjects: list[Subject] = []

    @property
    def subjects_count(self) -> int:
        return len(self._subjects)

    @property
    def subjects(self) -> list[Subject]:
        return list(self._subjects)

    def assign_subject(self, subject: Subject | Any) -> None:
        if not self.can_teach(subject):
            self._subjects.append(subject)

    def remove_subject(self, subject: Subject | Any) -> None:
        name = getattr(subject, "name", str(subject))
        self._subjects = [
            s for s in self._subjects if getattr(s, "name", str(s)) != name
        ]

    def update_degree(self, new_degree: str) -> None:
        if not new_degree.strip():
            raise ValueError("Ученая степень не может быть пустой строкой")
        self.degree = new_degree

    def can_teach(self, subject: Subject | Any) -> bool:
        name = getattr(subject, "name", str(subject))
        return any(getattr(s, "name", str(s)) == name for s in self._subjects)
