from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import DuplicateEnrollmentException
from lab2.domain.structure.speciality import Speciality

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class AcademicGroup:
    """
    Академическая учебная группа студентов.

    Attributes:
        number (str): Номер группы (например, "521702").
        speciality (Speciality): Специальность, к которой прикреплена группа.
        max_students (int): Максимально допустимое количество студентов.
    """
    DEFAULT_MAX_STUDENTS = 30

    def __init__(self, number: str, speciality: Speciality, max_students: int = DEFAULT_MAX_STUDENTS) -> None:
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
        return self._students.copy()

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

    def enroll_student(self, student: Student) -> None:
        """
        Зачисляет студента в группу.

        Args:
            student: Объект зачисляемого студента.

        Raises:
            ValueError: Если группа переполнена.
            DuplicateEnrollmentException: Если студент уже числится в этой группе.
        """
        if self.is_full():
            raise ValueError(f"Группа {self.number} переполнена. Лимит: {self.max_students}")

        if student in self._students:
            raise DuplicateEnrollmentException(f"Студент уже числится в группе {self.number}")

        self._students.append(student)
        student.group = self

    def expel_student(self, student: Student) -> None:
        """
        Исключает студента из списка группы.

        Args:
            student: Объект отчисляемого студента.

        Raises:
            ValueError: Если студент не найден в группе (выбрасывается встроенным методом list.remove).
        """
        self._students.remove(student)
        if getattr(student, "group", None) == self:
            student.group = None

    def clear_expelled(self) -> None:
        """Массовая очистка группы от отчисленных студентов (вызывается при подведении итогов)."""
        self._students = self.active_students

    def __str__(self) -> str:
        return f"Группа {self.number} ({self.students_count}/{self.max_students} чел.)"
