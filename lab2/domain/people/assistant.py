from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.people.lecturer import Lecturer

if TYPE_CHECKING:
    from lab2.domain.academics.labwork import LabWork
    from lab2.domain.academics.subject import Subject
    from lab2.domain.people.student import Student
    from lab2.domain.schedule.classroom import Classroom
    from lab2.domain.structure.academic_group import AcademicGroup


class Assistant(Lecturer):
    DEFAULT_POSITION = "Преподаватель"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = "Магистр",
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

    def conduct_lab(self, subject: Subject, lab: LabWork, group: AcademicGroup) -> str:
        return (
            f"Ассистент {self.full_name} провел лабораторную работу '{lab.title}' "
            f"по дисциплине '{subject.name}' в группе {group.number}."
        )

    def grade_labwork(self, student: Student, lab: LabWork, score: float) -> float:
        if not (0 <= score <= lab.max_score):
            raise ValueError(
                f"Оценка {score} выходит за пределы шкалы лабораторной (0 - {lab.max_score})."
            )
        return score

    def prepare_lab_equipment(self, classroom: Classroom) -> bool:
        if not classroom.is_available:
            raise ValueError(f"Аудитория {classroom.number} недоступна для подготовки.")
        return classroom.has_computers
