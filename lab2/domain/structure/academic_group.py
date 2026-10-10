from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import DuplicateEnrollmentException
from lab2.domain.structure.speciality import Speciality

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class AcademicGroup:
    DEFAULT_MAX_STUDENTS = 30

    def __init__(self, number: str, speciality: Speciality, max_students: int = DEFAULT_MAX_STUDENTS) -> None:
        self.number = number
        self.speciality = speciality
        self.max_students = max_students
        self._students: list[Student] = []

    @property
    def students_count(self) -> int:
        return len(self._students)

    @property
    def students(self) -> list[Student]:
        return self._students.copy()

    @property
    def active_students(self) -> list[Student]:
        return [s for s in self._students if s.is_active]

    @property
    def has_vacancies(self) -> bool:
        return self.students_count < self.max_students

    def is_full(self) -> bool:
        return not self.has_vacancies

    def enroll_student(self, student: Student) -> None:
        if self.is_full():
            raise ValueError(f"Группа {self.number} переполнена. Лимит: {self.max_students}")
        if student in self._students:
            raise DuplicateEnrollmentException(f"Студент уже числится в группе {self.number}")
        self._students.append(student)
        student.group = self

    def expel_student(self, student: Student) -> None:
        self._students.remove(student)
        if getattr(student, "group", None) == self:
            student.group = None

    def clear_expelled(self) -> None:
        self._students = self.active_students

    def __str__(self) -> str:
        return f"Группа {self.number} ({self.students_count}/{self.max_students} чел.)"
