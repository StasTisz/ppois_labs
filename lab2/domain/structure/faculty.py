from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import GroupNotFoundException
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.department import Department

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class Faculty:
    def __init__(self, name: str, short_name: str) -> None:
        self.name = name
        self.short_name = short_name
        self._departments: list[Department] = []
        self._groups: list[AcademicGroup] = []

    @property
    def departments(self) -> list[Department]:
        return list(self._departments)

    @property
    def groups(self) -> list[AcademicGroup]:
        return list(self._groups)

    def add_department(self, department: Department) -> None:
        self._departments.append(department)

    def add_group(self, group: AcademicGroup) -> None:
        if self.find_group(group.number):
            raise ValueError(
                f"Группа {group.number} уже существует на {self.short_name}"
            )
        self._groups.append(group)

    def find_group(self, number: str) -> AcademicGroup | None:
        for group in self._groups:
            if group.number == number:
                return group
        return None

    def get_group_strict(self, number: str) -> AcademicGroup:
        group = self.find_group(number)
        if not group:
            raise GroupNotFoundException(
                f"Группа {number} не найдена на факультете {self.short_name}"
            )
        return group

    def get_total_capacity(self) -> int:
        return sum(group.max_students for group in self._groups)

    def find_student_by_record_book(self, record_book_number: str) -> Student | None:
        for group in self._groups:
            for student in group.students:
                if student.record_book_number == record_book_number:
                    return student
        return None

    def find_student_by_id(self, student_id: str) -> Student | None:
        for group in self._groups:
            for student in group.students:
                if (
                    student.passport_number == student_id
                    or getattr(student, "person_id", None) == student_id
                    or student.record_book_number == student_id
                ):
                    return student
        return None

    def __repr__(self) -> str:
        return f"Faculty(name={self.short_name!r}, groups={len(self._groups)}, depts={len(self._departments)})"
