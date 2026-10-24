"""Модуль расписания учебных занятий."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import ScheduleCollisionException
from lab2.domain.schedule.lesson import Lesson

if TYPE_CHECKING:
    from lab2.domain.people.lecturer import Lecturer
    from lab2.domain.schedule.classroom import Classroom
    from lab2.domain.structure.academic_group import AcademicGroup


class Timetable:
    """Сводное расписание занятий на семестр."""

    def __init__(
        self,
        semester_number: int,
        academic_year: str = "2023/2024",
        faculty_name: str = "ФИТиУ",
    ) -> None:
        """Инициализирует экземпляр класса Timetable."""
        self.semester_number = semester_number
        self.academic_year = academic_year
        self.faculty_name = faculty_name
        self._lessons: list[Lesson] = []

    @property
    def lessons(self) -> list[Lesson]:
        """Возвращает значение атрибута lessons."""
        return list(self._lessons)

    def _check_collision(self, existing: Lesson, lesson: Lesson) -> None:
        """Проверяет отсутствие коллизий по преподавателю, аудитории или группе."""
        if not (
            existing.day_of_week == lesson.day_of_week
            and existing.timeslot.conflicts_with(lesson.timeslot)
        ):
            return

        if existing.room == lesson.room:
            raise ScheduleCollisionException(
                f"Накладка: аудитория {lesson.room.number} уже занята"
            )
        if existing.group == lesson.group:
            raise ScheduleCollisionException(
                f"Накладка: у группы {lesson.group.number} уже есть пара в это время"
            )
        if existing.lecturer == lesson.lecturer:
            raise ScheduleCollisionException(
                f"Накладка: преподаватель {lesson.lecturer.full_name} уже ведет пару"
            )

    def _validate_no_collisions(self, lesson: Lesson) -> None:
        """Внутренний валидатор: проверяет расписание на отсутствие накладок (коллизий)."""
        if not lesson.room.is_available:
            raise ScheduleCollisionException(
                f"Аудитория {lesson.room.number} закрыта на ремонт"
            )
        for existing in self._lessons:
            self._check_collision(existing, lesson)

    def add_lesson(self, lesson: Lesson) -> None:
        """Добавляет новое занятие в расписание."""
        self._validate_no_collisions(lesson)
        self._lessons.append(lesson)

    def remove_lesson(self, lesson: Lesson) -> None:
        """Удаляет указанное занятие из расписания."""
        if lesson in self._lessons:
            self._lessons.remove(lesson)

    def get_schedule_for_group(
        self, group: AcademicGroup, day_of_week: int
    ) -> list[Lesson]:
        """Фильтрация: получает расписание группы на конкретный день."""
        day_schedule = [
            lesson
            for lesson in self._lessons
            if lesson.group == group and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda item: item.timeslot.sequence_number)

    def get_lecturer_schedule(
        self, lecturer: Lecturer, day_of_week: int
    ) -> list[Lesson]:
        """Фильтрация: получает расписание преподавателя на конкретный день."""
        day_schedule = [
            lesson
            for lesson in self._lessons
            if lesson.lecturer == lecturer and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda item: item.timeslot.sequence_number)

    def get_classroom_schedule(self, room: Classroom, day_of_week: int) -> list[Lesson]:
        """Возвращает список всех занятий, проходящих в указанной аудитории."""
        day_schedule = [
            lesson
            for lesson in self._lessons
            if lesson.room == room and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda item: item.timeslot.sequence_number)

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return (
            f"Timetable(sem={self.semester_number}, lessons_count={len(self._lessons)})"
        )
