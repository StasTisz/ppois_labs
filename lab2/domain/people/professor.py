from __future__ import annotations

from lab2.domain.people.lecturer import Lecturer


class Professor(Lecturer):
    """
    Профессор кафедры. Высший академический статус, как правило, имеет степень доктора наук.
    """
    DEFAULT_DEGREE = "Д.т.н."

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, degree=degree)
