from __future__ import annotations


class Speciality:
    DEFAULT_SEMESTERS = 8
    MIN_SEMESTERS = 2
    MAX_SEMESTERS = 12

    def __init__(
        self,
        code: str,
        name: str,
        semesters_count: int = DEFAULT_SEMESTERS,
        qualification: str = "Инженер-системотехник",
        faculty_name: str = "ФИТиУ",
    ) -> None:
        self.code = code
        self.name = name
        self.semesters_count = semesters_count
        self.qualification = qualification
        self.faculty_name = faculty_name

    def update_semesters_count(self, new_count: int) -> None:
        if not (self.MIN_SEMESTERS <= new_count <= self.MAX_SEMESTERS):
            raise ValueError(
                f"Недопустимое количество семестров. "
                f"Допустимо от {self.MIN_SEMESTERS} до {self.MAX_SEMESTERS}."
            )
        self.semesters_count = new_count

    def rename(self, new_name: str) -> None:
        if not new_name.strip():
            raise ValueError("Название специальности не может быть пустым.")
        self.name = new_name

    def is_bachelor(self) -> bool:
        return self.semesters_count in (8, 9)

    def __str__(self) -> str:
        return f"[{self.code}] {self.name}"

    def __repr__(self) -> str:
        return f"Speciality(code={self.code!r}, name={self.name!r}, sems={self.semesters_count})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Speciality):
            return NotImplemented
        return self.code == other.code

    def __hash__(self) -> int:
        return hash(self.code)
