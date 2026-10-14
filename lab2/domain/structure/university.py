from __future__ import annotations

from lab2.domain.structure.faculty import Faculty


class University:
    DEFAULT_FOUNDED_YEAR = 1964
    DEFAULT_RECTOR = "Богуш В.А."

    def __init__(
        self,
        name: str,
        abbreviation: str,
        founded_year: int = DEFAULT_FOUNDED_YEAR,
        rector_name: str = DEFAULT_RECTOR,
    ) -> None:
        self.name = name
        self.abbreviation = abbreviation
        self.founded_year = founded_year
        self.rector_name = rector_name
        self._faculties: list[Faculty] = []

    @property
    def faculties(self) -> list[Faculty]:
        return list(self._faculties)

    def add_faculty(self, faculty: Faculty) -> None:
        if self.find_faculty(faculty.short_name):
            raise ValueError(
                f"Факультет '{faculty.short_name}' уже зарегистрирован в {self.abbreviation}"
            )
        self._faculties.append(faculty)

    def find_faculty(self, short_name: str) -> Faculty | None:
        for faculty_item in self._faculties:
            if faculty_item.short_name == short_name:
                return faculty_item
        return None

    def get_all_students_count(self) -> int:
        return sum(
            sum(group.students_count for group in faculty.groups)
            for faculty in self._faculties
        )

    def __repr__(self) -> str:
        return (
            f"University(abbr={self.abbreviation!r}, faculties={len(self._faculties)})"
        )
