"""Модуль преподавателя кафедры."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from lab2.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.structure.department import Department


class Lecturer(Employee):
    """Преподаватель университета (базовый класс для профильных преподавателей)."""

    DEFAULT_DEGREE = "Без степени"
    DEFAULT_POSITION = "Преподаватель"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = DEFAULT_DEGREE,
        position: str = DEFAULT_POSITION,
        passport_number: str = "",
        **kwargs: Any,
    ) -> None:
        """Инициализирует экземпляр класса Lecturer."""
        super().__init__(
            first_name,
            last_name,
            middle_name,
            position=position,
            passport_number=passport_number,
        )
        self.degree = degree
        self.department: Department | None = None
        self._subjects: list[Subject] = []

    @property
    def subjects_count(self) -> int:
        """Агрегация: количество читаемых преподавателем дисциплин."""
        return len(self._subjects)

    @property
    def subjects(self) -> list[Subject]:
        """Возвращает значение атрибута subjects."""
        return list(self._subjects)

    def assign_subject(self, subject: Subject) -> None:
        """Назначает преподавателю новую дисциплину для ведения.
        Защищает от дублирования одной и той же дисциплины."""
        if not self.can_teach(subject):
            self._subjects.append(subject)

    def remove_subject(self, subject: Subject) -> None:
        """Удаляет учебную дисциплину из педагогической нагрузки преподавателя."""
        self._subjects = [subj for subj in self._subjects if subj != subject]

    def update_degree(self, new_degree: str) -> None:
        """Обновляет ученую степень преподавателя (например, после защиты диссертации)."""
        if not new_degree.strip():
            raise ValueError("Ученая степень не может быть пустой строкой")
        self.degree = new_degree

    def can_teach(self, subject: Subject) -> bool:
        """Проверяет компетенцию: ведет ли преподаватель указанную дисциплину."""
        return any(subj == subject for subj in self._subjects)
