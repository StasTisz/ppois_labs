from __future__ import annotations

from datetime import UTC, datetime

from lab2.domain.academics.subject import Subject
from lab2.domain.exceptions import InvalidScoreException


class Grade:
    MIN_SCORE = 0
    MAX_SCORE = 10
    MIN_PASSING_SCORE = 4

    def __init__(self, subject: Subject | str, score: int, is_exam: bool = False) -> None:
        if isinstance(subject, str):
            self.subject: Subject | None = None
            self.subject_name = subject
        else:
            self.subject = subject
            self.subject_name = subject.name
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
    def is_passed(self) -> bool:
        return self.score >= self.MIN_PASSING_SCORE
