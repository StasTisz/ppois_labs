from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from lab2.domain.academics.subject import Subject
from lab2.domain.exceptions import InvalidScoreException

if TYPE_CHECKING:
    from lab2.domain.people.employee import Employee


class Grade:
    MIN_SCORE = 0
    MAX_SCORE = 10
    MIN_PASSING_SCORE = 4

    def __init__(
        self,
        subject: Subject,
        score: int,
        is_exam: bool = False,
        examiner: Employee | None = None,
    ) -> None:
        self.subject = subject
        self.examiner = examiner
        self.score = score
        self.is_exam = is_exam
        self.date_issued = datetime.now(UTC)
        self._validate_score()

    def _validate_score(self) -> None:
        if not (self.MIN_SCORE <= self.score <= self.MAX_SCORE):
            raise InvalidScoreException(
                f"Недопустимый балл: {self.score}. В системе оценок допустимы "
                f"значения от {self.MIN_SCORE} до {self.MAX_SCORE}."
            )

    @property
    def subject_name(self) -> str:
        if hasattr(self.subject, "name"):
            return self.subject.name
        return str(self.subject)

    @property
    def is_passed(self) -> bool:
        return self.score >= self.MIN_PASSING_SCORE

    def assign_examiner(self, examiner: Employee) -> None:
        self.examiner = examiner

    def update_score(self, new_score: int) -> None:
        self.score = new_score
        self._validate_score()

    def __repr__(self) -> str:
        examiner_str = self.examiner.full_name if self.examiner else "None"
        return f"Grade(subject={self.subject_name!r}, score={self.score}, is_exam={self.is_exam}, examiner={examiner_str!r})"
