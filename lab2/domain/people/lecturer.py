from __future__ import annotations

from typing import Any

from lab2.domain.people.employee import Employee


class Lecturer(Employee):
    """
    Преподаватель университета (базовый класс для профильных преподавателей).

    Attributes:
        degree (str): Ученая степень.
    """
    DEFAULT_DEGREE = "Без степени"
    DEFAULT_POSITION = "Преподаватель"

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, position=self.DEFAULT_POSITION)
        self.degree = degree
        self.department: Any = None
        self._subjects: list[Any] = []

    @property
    def subjects_count(self) -> int:
        """Агрегация: количество читаемых преподавателем дисциплин."""
        return len(self._subjects)

    def assign_subject(self, subject: Any) -> None:
        """
        Назначает преподавателю новую дисциплину для ведения.
        Защищает от дублирования одной и той же дисциплины.

        Args:
            subject: Название дисциплины или экземпляр Subject.
        """
        name = getattr(subject, "name", str(subject))
        if not self.can_teach(name):
            self._subjects.append(subject)

    def update_degree(self, new_degree: str) -> None:
        """
        Обновляет ученую степень преподавателя (например, после защиты диссертации).

        Raises:
            ValueError: Если передана пустая строка.
        """
        if not new_degree.strip():
            raise ValueError("Ученая степень не может быть пустой строкой")
        self.degree = new_degree

    def can_teach(self, subject: Any) -> bool:
        """
        Проверяет компетенцию: ведет ли преподаватель указанную дисциплину.
        """
        name = getattr(subject, "name", str(subject))
        return any(getattr(s, "name", str(s)) == name for s in self._subjects)
