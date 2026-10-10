from __future__ import annotations

from lab2.domain.exceptions import ScheduleCollisionException
from lab2.domain.people.lecturer import Lecturer
from lab2.domain.schedule.lesson import Lesson
from lab2.domain.structure.academic_group import AcademicGroup


class Timetable:
    def __init__(self, semester_number: int) -> None:
        self.semester_number = semester_number
        self._lessons: list[Lesson] = []

    def _validate_no_collisions(self, lesson: Lesson) -> None:
        if not lesson.room.is_available:
            raise ScheduleCollisionException(f"Аудитория {lesson.room.number} закрыта на ремонт")

        for existing in self._lessons:
            if existing.day_of_week == lesson.day_of_week and                     existing.timeslot.sequence_number == lesson.timeslot.sequence_number:
                if existing.room.number == lesson.room.number:
                    raise ScheduleCollisionException(f"Накладка: аудитория {lesson.room.number} уже занята")
                if existing.group.number == lesson.group.number:
                    raise ScheduleCollisionException(f"Накладка: у группы {lesson.group.number} уже есть пара в это время")
                if existing.lecturer.person_id == lesson.lecturer.person_id:
                    raise ScheduleCollisionException(f"Накладка: преподаватель {lesson.lecturer.full_name} уже ведет пару")

    def add_lesson(self, lesson: Lesson) -> None:
        self._validate_no_collisions(lesson)
        self._lessons.append(lesson)

    def get_schedule_for_group(self, group: AcademicGroup | str, day_of_week: int) -> list[Lesson]:
        group_num = group.number if isinstance(group, AcademicGroup) else group
        day_schedule = [
            lesson for lesson in self._lessons
            if lesson.group.number == group_num and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)

    def get_lecturer_schedule(self, lecturer: Lecturer | str, day_of_week: int) -> list[Lesson]:
        lecturer_id = lecturer.person_id if isinstance(lecturer, Lecturer) else lecturer
        day_schedule = [
            lesson for lesson in self._lessons
            if lesson.lecturer.person_id == lecturer_id and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)
