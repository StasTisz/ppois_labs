"""Модуль академической учебной группы."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import DuplicateEnrollmentException
from lab2.domain.structure.speciality import Speciality

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class AcademicGroup:
    """Академическая учебная группа студентов."""

    DEFAULT_MAX_STUDENTS = 30

    def __init__(
        self,
        number: str,
        speciality: Speciality,
        max_students: int = DEFAULT_MAX_STUDENTS,
    ) -> None:
        """Инициализирует экземпляр класса AcademicGroup."""
        self.number = number
        self.speciality = speciality
        self.max_students = max_students
        self._students: list[Student] = []

    @property
    def students_count(self) -> int:
        """Возвращает текущее количество студентов в группе."""
        return len(self._students)

    @property
    def students(self) -> list[Student]:
        """Возвращает защищенную копию списка студентов."""
        return list(self._students)

    @property
    def active_students(self) -> list[Student]:
        """Возвращает список только тех студентов, кто не отчислен."""
        return [s for s in self._students if s.is_active]

    @property
    def has_vacancies(self) -> bool:
        """Проверка наличия свободных мест в группе."""
        return self.students_count < self.max_students

    def is_full(self) -> bool:
        """Проверяет, достигнут ли лимит вместимости группы."""
        return not self.has_vacancies

    def has_student(self, student: Student) -> bool:
        """Проверяет факт числящегося студента в составе академической группы."""
        return student in self._students

    def enroll_student(self, student: Student) -> None:
        """Зачисляет студента в группу."""
        if self.is_full():
            raise ValueError(
                f"Группа {self.number} переполнена. Лимит: {self.max_students}"
            )
        if self.has_student(student):
            raise DuplicateEnrollmentException(
                f"Студент уже числится в группе {self.number}"
            )
        self._students.append(student)
        student.group = self

    def expel_student(self, student: Student) -> None:
        """Исключает студента из списка группы."""
        if student in self._students:
            self._students.remove(student)
            if getattr(student, "group", None) == self:
                student.group = None

    def clear_expelled(self) -> None:
        """Массовая очистка группы от отчисленных студентов (вызывается при подведении итогов)."""
        for student in list(self._students):
            if not student.is_active:
                self.expel_student(student)

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return f"Группа {self.number} ({self.students_count}/{self.max_students} чел.)"

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"AcademicGroup(number={self.number!r}, spec={self.speciality.name!r}, students={self.students_count})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, AcademicGroup):
            return NotImplemented
        return self.number == other.number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.number)
