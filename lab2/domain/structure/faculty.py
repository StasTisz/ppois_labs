from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import GroupNotFoundException
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.department import Department

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class Faculty:
    """
    Учебный факультет университета.

    Attributes:
        name (str): Полное название факультета.
        short_name (str): Аббревиатура факультета (например, "ФИТиУ").
    """
    def __init__(self, name: str, short_name: str) -> None:
        self.name = name
        self.short_name = short_name
        self._departments: list[Department] = []
        self._groups: list[AcademicGroup] = []

    @property
    def groups(self) -> list[AcademicGroup]:
        """Возвращает защищенную копию списка групп."""
        return self._groups.copy()

    def add_department(self, department: Department) -> None:
        """Прикрепляет кафедру к факультету."""
        self._departments.append(department)

    def add_group(self, group: AcademicGroup) -> None:
        """
        Регистрирует новую академическую группу на факультете.

        Args:
            group: Объект добавляемой группы.

        Raises:
            ValueError: Если группа с таким номером уже существует.
        """
        if self.find_group(group.number):
            raise ValueError(f"Группа {group.number} уже существует на {self.short_name}")
        self._groups.append(group)

    def find_group(self, number: str) -> AcademicGroup | None:
        """
        Мягкий поиск группы по номеру (возвращает None, если не найдена).
        """
        for group in self._groups:
            if group.number == number:
                return group
        return None

    def get_group_strict(self, number: str) -> AcademicGroup:
        """
        Строгий поиск группы по номеру (для бизнес-логики, требующей гарантии существования).

        Raises:
            GroupNotFoundException: Если группа не найдена.
        """
        group = self.find_group(number)
        if not group:
            raise GroupNotFoundException(f"Группа {number} не найдена на факультете {self.short_name}")
        return group

    def get_total_capacity(self) -> int:
        """Подсчитывает максимальную суммарную вместимость всех групп факультета."""
        return sum(group.max_students for group in self._groups)

    def find_student_by_id(self, person_id: str) -> Student | None:
        """
        Сквозной поиск студента по номеру билета/идентификатору среди всех групп факультета.
        """
        for group in self._groups:
            for student in group.students:
                if getattr(student, 'person_id', None) == person_id:
                    return student
        return None
