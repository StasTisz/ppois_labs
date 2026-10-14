from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.grading.grade import Grade

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.people.lecturer import Lecturer
    from lab2.domain.people.student import Student


class RetakeSheet:
    DEFAULT_MAX_ATTEMPTS = 3

    def __init__(
        self,
        student: Student,
        subject: Subject,
        examiner: Lecturer | None = None,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        sheet_number: str = "",
    ) -> None:
        self.sheet_number = (
            sheet_number
            or f"RS-{abs(hash((student.record_book_number, subject.name))) % 100000:05d}"
        )
        self.student = student
        self.subject = subject
        self.examiner = examiner
        self.max_attempts = max_attempts
        self.attempts_used = 0
        self._is_valid = True

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def remaining_attempts(self) -> int:
        return max(0, self.max_attempts - self.attempts_used)

    def assign_examiner(self, examiner: Lecturer) -> None:
        self.examiner = examiner

    def invalidate(self) -> None:
        self._is_valid = False

    def register_attempt(self, score: int, examiner: Lecturer | None = None) -> Grade:
        if not self._is_valid:
            raise ValueError("Бегунок просрочен или лимит попыток исчерпан.")
        effective_examiner = examiner or self.examiner
        self.attempts_used += 1
        if self.attempts_used >= self.max_attempts:
            self._is_valid = False
        return Grade(self.subject, score, is_exam=True, examiner=effective_examiner)

    def __repr__(self) -> str:
        return f"RetakeSheet(num={self.sheet_number!r}, student={self.student.full_name!r}, subject={self.subject.name!r}, attempts={self.attempts_used}/{self.max_attempts})"
