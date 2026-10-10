from __future__ import annotations

import uuid
from typing import Any

from lab2.domain.academics.subject import Subject

from lab2.domain.grading.grade import Grade
from lab2.domain.people.lecturer import Lecturer
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup


class AcademicStatement:
    """
    Экзаменационная ведомость группы для конкретной дисциплины.

    Attributes:
        statement_id (str): Уникальный номер ведомости.
        subject (Subject): Учебная дисциплина.
        group (AcademicGroup): Экзаменуемая группа.
        examiner (Lecturer): Преподаватель, принимающий экзамен.
        is_closed (bool): Статус документа (закрыт/открыт).
    """

    def __init__(self, subject: Subject, group: AcademicGroup, examiner: Lecturer) -> None:
        self.statement_id = str(uuid.uuid4())
        self.subject = subject
        self.group = group
        self.examiner = examiner
        self.is_closed = False
        self._results: dict[Any, Grade] = {}

    def add_result(self, student: Student, score: int) -> None:
        """
        Вносит оценку конкретного студента в ведомость.

        Args:
            student (Student): Сдающий студент.
            score (int): Выставленный балл.

        Raises:
            ValueError: Если ведомость уже закрыта.
        """
        if self.is_closed:
            raise ValueError("Ведомость уже закрыта и передана в деканат.")

        grade = Grade(self.subject, score, is_exam=True)
        self._results[student] = grade
        self._results[student.person_id] = grade

    def close_statement(self) -> None:
        """Блокирует ведомость от дальнейших изменений."""
        self.is_closed = True

    @property
    def pass_rate(self) -> float:
        """Агрегация: вычисляет процент успешной сдачи (успеваемость группы)."""
        grades = [v for k, v in self._results.items() if not isinstance(k, str)] or list(self._results.values())
        if not grades:
            return 0.0
        passed = sum(1 for grade in grades if grade.is_passed)
        return round((passed / len(grades)) * 100, 2)
