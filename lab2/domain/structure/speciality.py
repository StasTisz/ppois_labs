"""Модуль специальности высшего образования."""

from __future__ import annotations


class Speciality:
    """Учебная специальность университета."""

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
        """Инициализирует экземпляр класса Speciality."""
        self.code = code
        self.name = name
        self.semesters_count = semesters_count
        self.qualification = qualification
        self.faculty_name = faculty_name

    def update_semesters_count(self, new_count: int) -> None:
        """Изменяет нормативный срок обучения по специальности."""
        if not (self.MIN_SEMESTERS <= new_count <= self.MAX_SEMESTERS):
            raise ValueError(
                f"Недопустимое количество семестров. "
                f"Допустимо от {self.MIN_SEMESTERS} до {self.MAX_SEMESTERS}."
            )
        self.semesters_count = new_count

    def rename(self, new_name: str) -> None:
        """Изменяет наименование специальности подготовки."""
        if not new_name.strip():
            raise ValueError("Название специальности не может быть пустым.")
        self.name = new_name

    def is_bachelor(self) -> bool:
        """Проверяет, относится ли специальность к программе бакалавриата."""
        return self.semesters_count in (8, 9)

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return f"[{self.code}] {self.name}"

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Speciality(code={self.code!r}, name={self.name!r}, sems={self.semesters_count})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Speciality):
            return NotImplemented
        return self.code == other.code

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.code)
