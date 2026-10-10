from __future__ import annotations

import uuid

from lab2.domain.academics.subject import Subject
from lab2.domain.people.lecturer import Lecturer
from lab2.domain.schedule.classroom import Classroom
from lab2.domain.schedule.timeslot import Timeslot
from lab2.domain.structure.academic_group import AcademicGroup


class Lesson:
    """
    Конкретное занятие в расписании, связывающее все сущности воедино.

    Attributes:
        lesson_id (str): Уникальный номер занятия в базе (UUID).
        subject (Subject): Изучаемая дисциплина.
        lecturer (Lecturer): Назначенный преподаватель.
        group (AcademicGroup): Учебная группа.
        room (Classroom): Аудитория для проведения.
        timeslot (Timeslot): Порядковый номер пары и время.
        day_of_week (int): День недели (1 - Понедельник, ..., 7 - Воскресенье).
    """

    def __init__(
            self, subject: Subject, lecturer: Lecturer, group: AcademicGroup, room: Classroom,
            timeslot: Timeslot, day_of_week: int
    ) -> None:
        self.lesson_id = str(uuid.uuid4())
        self.subject = subject
        self.lecturer = lecturer
        self.group = group
        self.room = room
        self.timeslot = timeslot
        self.day_of_week = day_of_week

        self._validate_capacity()
        self._validate_room_equipment()

    def _validate_capacity(self) -> None:
        """
        Внутренний валидатор: проверяет, поместится ли группа в аудиторию.

        Raises:
            ValueError: Если размер группы превышает вместимость.
        """
        if self.group.students_count > self.room.capacity:
            raise ValueError(
                f"Аудитория {self.room.number} ({self.room.capacity} мест) мала "
                f"для группы {self.group.number} ({self.group.students_count} чел.)"
            )

    def _validate_room_equipment(self) -> None:
        """
        Внутренний валидатор: проверяет техническое оснащение аудитории под специфику предмета.

        Raises:
            ValueError: Если для лабораторной работы выделена аудитория без ПК.
        """
        if "лабораторн" in self.subject.name.lower() and not self.room.has_computers:
            raise ValueError(f"Для предмета {self.subject.name} нужна компьютерная аудитория")
