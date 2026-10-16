"""Модуль профессора кафедры."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.people.lecturer import Lecturer

if TYPE_CHECKING:
    from lab2.domain.people.student import Student
    from lab2.domain.structure.academic_group import AcademicGroup


class Professor(Lecturer):
    """Профессор кафедры. Высший академический статус, как правило, имеет степень доктора наук."""

    DEFAULT_DEGREE = "Д.т.н."
    DEFAULT_POSITION = "Профессор"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = DEFAULT_DEGREE,
        passport_number: str = "",
        doctoral_students_count: int = 2,
    ) -> None:
        """Инициализирует экземпляр класса Professor."""
        super().__init__(
            first_name,
            last_name,
            middle_name,
            degree=degree,
            position=self.DEFAULT_POSITION,
            passport_number=passport_number,
        )
        self.doctoral_students_count = doctoral_students_count
        self.advisees: list[Student] = []

    def assign_advisee(self, student: Student) -> None:
        """Назначает студента подопечным дипломником или аспирантом."""
        if student not in self.advisees:
            self.advisees.append(student)

    def supervise_graduate(self, student: Student, thesis_title: str) -> str:
        """Осуществляет научное руководство дипломником или аспирантом."""
        if not student.is_active:
            raise ValueError(
                f"Нельзя руководить дипломом отчисленного студента {student.full_name}"
            )
        return f"Профессор {self.full_name} утвержден научным руководителем студента {student.full_name} по теме '{thesis_title}'."

    def chair_defense_committee(self, group: AcademicGroup) -> str:
        """Возглавляет комиссию по защите дипломных проектов."""
        return f"Профессор {self.full_name} возглавил государственную экзаменационную комиссию группы {group.number}."

    def conduct_scientific_seminar(self, topic: str) -> str:
        """Проводит научно-исследовательский семинар для кафедры."""
        if not topic.strip():
            raise ValueError("Тема семинара не может быть пустой.")
        return f"Профессор {self.full_name} провел межкафедральный научный семинар на тему '{topic}'."
