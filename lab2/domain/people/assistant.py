from __future__ import annotations

from lab2.domain.people.lecturer import Lecturer


class Assistant(Lecturer):
    """
    Ассистент кафедры. Обычно ведет лабораторные и практические занятия.
    """
    DEFAULT_DEGREE = "Магистр"

    def __init__(self, first_name: str, last_name: str, middle_name: str = "") -> None:
        super().__init__(first_name, last_name, middle_name, degree=self.DEFAULT_DEGREE)
