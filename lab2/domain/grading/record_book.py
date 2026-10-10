from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.grading.grade import Grade

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.people.student import Student


class RecordBook:
    """
    Зачетная книжка конкретного студента, хранящая историю всех оценок.

    Attributes:
        student (Student | None): Владелец зачетной книжки (экземпляр Student).
        student_id (str): Идентификатор владельца (Student.person_id).
        book_number (str): Уникальный номер бланка зачетной книжки.
    """

    def __init__(self, student: Student | str, book_number: str) -> None:
        self.student = student if not isinstance(student, str) else None
        self._student_id = getattr(student, "person_id", str(student))
        self.book_number = book_number
        self._grades: list[Grade] = []
        if hasattr(student, "record_book"):
            student.record_book = self

    @property
    def student_id(self) -> str:
        if self.student is not None:
            return self.student.person_id
        return self._student_id

    def add_grade(self, grade: Grade) -> None:
        """
        Вносит новую оценку в зачетную книжку.

        Args:
            grade (Grade): Объект выставляемой оценки.

        Raises:
            ValueError: Если экзаменационная оценка по этому предмету уже стоит.
        """
        if grade.is_exam and any(g.subject_name == grade.subject_name and g.is_exam for g in self._grades):
            raise ValueError(f"Экзаменационная оценка по {grade.subject_name} уже стоит в зачетке {self.book_number}")
        self._grades.append(grade)

    @property
    def average_score(self) -> float:
        """Агрегация: вычисляет средний балл по всем записям."""
        if not self._grades:
            return 0.0
        total = sum(g.score for g in self._grades)
        return round(total / len(self._grades), 2)

    def get_debts(self) -> list[str]:
        """
        Анализ успеваемости: формирует список предметов с академической задолженностью.

        Returns:
            list[str]: Названия несданных дисциплин.
        """
        return [grade.subject_name for grade in self._grades if not grade.is_passed]

    def clear_debts_for_subject(self, subject: Subject | str) -> None:
        """
        Удаляет неудовлетворительные оценки по предмету после успешной пересдачи.

        Args:
            subject (Subject | str): Предмет или его название, по которому закрыт долг.
        """
        subj_name = subject.name if hasattr(subject, "name") else str(subject)
        self._grades = [g for g in self._grades if not (g.subject_name == subj_name and not g.is_passed)]

    @property
    def is_excellent(self) -> bool:
        """Бизнес-правило: является ли студент круглым отличником (все оценки >= 9)."""
        if not self._grades:
            return False
        return all(g.score >= 9 for g in self._grades)

    def get_best_subject(self) -> str | None:
        """
        Ищет предмет с максимальным баллом.

        Returns:
            str | None: Название предмета или None, если оценок нет.
        """
        if not self._grades:
            return None
        best_grade = max(self._grades, key=lambda g: g.score)
        return best_grade.subject_name
