from __future__ import annotations

from lab2.domain.people.lecturer import Lecturer


class AssociateProfessor(Lecturer):
    DEFAULT_DEGREE = "К.т.н."

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, degree=degree)
