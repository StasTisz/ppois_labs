from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.people.lecturer import Lecturer

if TYPE_CHECKING:
    from lab2.domain.people.student import Student
    from lab2.domain.structure.academic_group import AcademicGroup


class Professor(Lecturer):
    DEFAULT_DEGREE = "Д.т.н."
    DEFAULT_POSITION = "Профессор"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = DEFAULT_DEGREE,
        passport_number: str = "",
    ) -> None:
        super().__init__(
            first_name,
            last_name,
            middle_name,
            degree=degree,
            position=self.DEFAULT_POSITION,
            passport_number=passport_number,
        )

    def supervise_graduate(self, student: Student, thesis_title: str) -> str:
        if not student.is_active:
            raise ValueError(
                f"Нельзя руководить дипломом отчисленного студента {student.full_name}"
            )
        return f"Профессор {self.full_name} утвержден научным руководителем студента {student.full_name} по теме '{thesis_title}'."

    def chair_defense_committee(self, group: AcademicGroup) -> str:
        return f"Профессор {self.full_name} возглавил государственную экзаменационную комиссию группы {group.number}."

    def conduct_scientific_seminar(self, topic: str) -> str:
        if not topic.strip():
            raise ValueError("Тема семинара не может быть пустой.")
        return f"Профессор {self.full_name} провел межкафедральный научный семинар на тему '{topic}'."
