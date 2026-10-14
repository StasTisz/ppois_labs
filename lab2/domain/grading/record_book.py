from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.grading.grade import Grade

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.people.student import Student


class RecordBook:
    EXCELLENT_GRADE_THRESHOLD = 9.0
    DEFAULT_ISSUE_DATE = "2023-09-01"

    def __init__(
        self,
        student: Student,
        book_number: str,
        issue_date: str = DEFAULT_ISSUE_DATE,
        academic_year: str = "2023/2024",
    ) -> None:
        self.student = student
        self.book_number = book_number
        self.issue_date = issue_date
        self.academic_year = academic_year
        self._grades: list[Grade] = []
        if hasattr(student, "record_book"):
            student.record_book = self

    @property
    def grades(self) -> list[Grade]:
        return list(self._grades)

    def add_grade(self, grade: Grade) -> None:
        if grade.is_exam and any(
            grade_item.subject == grade.subject and grade_item.is_exam
            for grade_item in self._grades
        ):
            raise ValueError(
                f"Экзаменационная оценка по {grade.subject_name} уже стоит в зачетке {self.book_number}"
            )
        self._grades.append(grade)

    @property
    def average_score(self) -> float:
        if not self._grades:
            return 0.0
        total = sum(grade_item.score for grade_item in self._grades)
        return round(total / len(self._grades), 2)

    def get_debts(self) -> list[str]:
        return [
            grade_item.subject_name
            for grade_item in self._grades
            if not grade_item.is_passed
        ]

    def clear_debts_for_subject(self, subject: Subject) -> None:
        self._grades = [
            grade_item
            for grade_item in self._grades
            if not (
                grade_item.subject == subject and not grade_item.is_passed
            )
        ]

    @property
    def is_excellent(self) -> bool:
        if not self._grades:
            return False
        return all(
            grade_item.score >= self.EXCELLENT_GRADE_THRESHOLD
            for grade_item in self._grades
        )

    def get_best_subject(self) -> str | None:
        if not self._grades:
            return None
        best_grade = max(self._grades, key=lambda grade_item: grade_item.score)
        return best_grade.subject_name

    def __repr__(self) -> str:
        return f"RecordBook(number={self.book_number!r}, student={self.student.full_name!r}, grades_count={len(self._grades)})"
