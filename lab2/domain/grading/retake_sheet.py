from __future__ import annotations

import uuid

from lab2.domain.academics.subject import Subject

from lab2.domain.grading.grade import Grade
from lab2.domain.people.student import Student


class RetakeSheet:
    """
    Индивидуальное направление на пересдачу («бегунок»).

    Attributes:
        sheet_id (str): Уникальный номер бланка.
        student (Student): Направляемый студент.
        subject (Subject): Дисциплина для пересдачи.
        max_attempts (int): Максимально разрешенное количество попыток.
        attempts_used (int): Использованное количество попыток.
        is_valid (bool): Действителен ли бегунок. False - просрочен
    """
    DEFAULT_MAX_ATTEMPTS = 3

    def __init__(self, student: Student, subject: Subject, max_attempts: int = DEFAULT_MAX_ATTEMPTS) -> None:
        self.sheet_id = str(uuid.uuid4())
        self.student = student
        self.subject = subject
        self.max_attempts = max_attempts
        self.attempts_used = 0
        self.is_valid = True

    def register_attempt(self, score: int) -> Grade:
        """
        Фиксирует попытку сдать экзамен по бегунку.

        Args:
            score (int): Полученный балл.

        Returns:
            Grade: Объект итоговой оценки.

        Raises:
            ValueError: Если лимит попыток исчерпан или бегунок недействителен.
        """
        if not self.is_valid:
            raise ValueError("Бегунок просрочен или лимит попыток исчерпан.")

        self.attempts_used += 1

        if self.attempts_used >= self.max_attempts:
            self.is_valid = False

        return Grade(self.subject, score, is_exam=True)
