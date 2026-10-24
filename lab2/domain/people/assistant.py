"""Модуль преподавателя-ассистента кафедры."""

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
    """Ассистент кафедры. Обычно ведет лабораторные и практические занятия."""

    DEFAULT_POSITION = "Преподаватель"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = "Магистр",
        passport_number: str = "",
        consultation_hours: int = 4,
        assigned_labs_count: int = 0,
    ) -> None:
        """Инициализирует экземпляр класса Assistant."""
        try:
            super().__init__(
                first_name,
                last_name,
                middle_name,
                degree=degree,
                position=self.DEFAULT_POSITION,
                passport_number=passport_number,
            )
        except TypeError:
            super().__init__(
                first_name,
                last_name,
                middle_name,
                degree=degree,
                passport_number=passport_number,
            )
        self.consultation_hours = consultation_hours
        self.assigned_labs_count = assigned_labs_count

    def record_labwork_completed(self) -> None:
        """Фиксирует успешное выполнение лабораторной работы студентом."""
        self.assigned_labs_count += 1

    def conduct_lab(self, subject: Subject, lab: LabWork, group: AcademicGroup) -> str:
        """Проводит лабораторное занятие для академической группы в аудитории."""
        return (
            f"Ассистент {self.full_name} провел лабораторную работу '{lab.title}' "
            f"по дисциплине '{subject.name}' в группе {group.number}."
        )

    def grade_labwork(self, student: Student, lab: LabWork, score: float) -> float:
        """Выставляет и регистрирует балл за лабораторную работу в ведомость."""
        if not (0 <= score <= lab.max_score):
            raise ValueError(
                f"Оценка {score} выходит за пределы шкалы лабораторной (0 - {lab.max_score})."
            )
        return score

    def prepare_lab_equipment(self, classroom: Classroom) -> bool:
        """Проверяет и подготавливает оборудование в лаборатории перед занятием."""
        if not classroom.is_available:
            raise ValueError(f"Аудитория {classroom.number} недоступна для подготовки.")
        return classroom.has_computers
