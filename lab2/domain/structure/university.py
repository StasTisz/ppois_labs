from __future__ import annotations

from lab2.domain.structure.faculty import Faculty


class University:
    """
    Университет как корневая структура предметной области.

    Attributes:
        name (str): Полное название учебного заведения.
        abbreviation (str): Краткая аббревиатура.
    """
    def __init__(self, name: str, abbreviation: str) -> None:
        self.name = name
        self.abbreviation = abbreviation
        self._faculties: list[Faculty] = []

    def add_faculty(self, faculty: Faculty) -> None:
        """
        Регистрирует новый факультет.

        Raises:
            ValueError: Если факультет с такой аббревиатурой уже существует.
        """
        if self.find_faculty(faculty.short_name):
            raise ValueError(f"Факультет '{faculty.short_name}' уже зарегистрирован в {self.abbreviation}")
        self._faculties.append(faculty)

    def find_faculty(self, short_name: str) -> Faculty | None:
        """Ищет факультет по аббревиатуре."""
        for f in self._faculties:
            if f.short_name == short_name:
                return f
        return None
