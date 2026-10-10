from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.grading.grade import Grade
from lab2.domain.people.student import Student

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject


class RecordBook:
    def __init__(self, student: Student | str, book_number: str) -> None:
        self.student = student if isinstance(student, Student) else None
        self._student_id = student.person_id if isinstance(student, Student) else str(student)
        self.book_number = book_number
        self._grades: list[Grade] = []
        if isinstance(student, Student):
            student.record_book = self

    @property
    def student_id(self) -> str:
        if self.student is not None:
            return self.student.person_id
        return self._student_id

    def add_grade(self, grade: Grade) -> None:
        if grade.is_exam and any(g.subject_name == grade.subject_name and g.is_exam for g in self._grades):
            raise ValueError(f"Экзаменационная оценка по {grade.subject_name} уже стоит в зачетке {self.book_number}")
        self._grades.append(grade)

    @property
    def average_score(self) -> float:
        if not self._grades:
            return 0.0
        total = sum(g.score for g in self._grades)
        return round(total / len(self._grades), 2)

    def get_debts(self) -> list[str]:
        return [grade.subject_name for grade in self._grades if not grade.is_passed]

    def clear_debts_for_subject(self, subject: Subject | str) -> None:
        subj_name = subject.name if hasattr(subject, "name") else str(subject)
        self._grades = [g for g in self._grades if not (g.subject_name == subj_name and not g.is_passed)]

    @property
    def is_excellent(self) -> bool:
        if not self._grades:
            return False
        return all(g.score >= 9 for g in self._grades)

    def get_best_subject(self) -> str | None:
        if not self._grades:
            return None
        best_grade = max(self._grades, key=lambda g: g.score)
        return best_grade.subject_name
