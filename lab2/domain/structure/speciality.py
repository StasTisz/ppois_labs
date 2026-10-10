from __future__ import annotations


class Speciality:
    """
    Учебная специальность университета.

    Attributes:
        code (str): Шифр специальности (например, "1-40 05 01").
        name (str): Полное наименование специальности.
        semesters_count (int): Нормативный срок обучения в семестрах.
    """
    DEFAULT_SEMESTERS = 8
    MIN_SEMESTERS = 2
    MAX_SEMESTERS = 12

    def __init__(self, code: str, name: str, semesters_count: int = DEFAULT_SEMESTERS) -> None:
        self.code = code
        self.name = name
        self.semesters_count = semesters_count

    def __str__(self) -> str:
        return f"[{self.code}] {self.name}"

    def update_semesters_count(self, new_count: int) -> None:
        """
        Изменяет нормативный срок обучения по специальности.

        Args:
            new_count (int): Новое количество семестров.

        Raises:
            ValueError: Если количество семестров выходит за допустимые границы.
        """
        if not (self.MIN_SEMESTERS <= new_count <= self.MAX_SEMESTERS):
            raise ValueError(
                f"Недопустимое количество семестров. "
                f"Допустимо от {self.MIN_SEMESTERS} до {self.MAX_SEMESTERS}."
            )
        self.semesters_count = new_count
