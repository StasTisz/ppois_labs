from __future__ import annotations

from datetime import datetime, timezone

from lab2.domain.academics.subject import Subject


class Grade:
    """
    Оценка за конкретный вид контроля (экзамен, зачет, лабораторная).

    Attributes:
        subject_name (str): Название дисциплины.
        subject (Subject | None): Экземпляр учебной дисциплины.
        score (int): Выставленный балл.
        is_exam (bool): Является ли оценка итоговой (экзаменационной).
        date_issued (datetime): Точное время выставления оценки (в UTC).
    """
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
        self.date_issued = datetime.now(timezone.utc)
        self._validate_score()

    def _validate_score(self) -> None:
        """
        Внутренний валидатор диапазона оценки.

        Raises:
            ValueError: Если балл выходит за допустимые границы (0-10).
        """
        if not (self.MIN_SCORE <= self.score <= self.MAX_SCORE):
            raise ValueError(
                f"Недопустимый балл: {self.score}. В системе оценок допустимы "
                f"значения от {self.MIN_SCORE} до {self.MAX_SCORE}."
            )

    @property
    def is_passed(self) -> bool:
        """Бизнес-правило: считается ли предмет сданным (4 балла и выше)."""
        return self.score >= self.MIN_PASSING_SCORE
