from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import ScheduleCollisionException
from lab2.domain.schedule.lesson import Lesson

if TYPE_CHECKING:
    from lab2.domain.people.lecturer import Lecturer
    from lab2.domain.schedule.classroom import Classroom
    from lab2.domain.structure.academic_group import AcademicGroup


class Timetable:
    def __init__(self, semester_number: int) -> None:
        self.semester_number = semester_number
        self._lessons: list[Lesson] = []

    @property
    def lessons(self) -> list[Lesson]:
        return list(self._lessons)

    def _validate_no_collisions(self, lesson: Lesson) -> None:
        if not lesson.room.is_available:
            raise ScheduleCollisionException(
                f"Аудитория {lesson.room.number} закрыта на ремонт"
            )

        for existing in self._lessons:
            if (
                existing.day_of_week == lesson.day_of_week
                and existing.timeslot.conflicts_with(lesson.timeslot)
            ):
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

    def add_lesson(self, lesson: Lesson) -> None:
        self._validate_no_collisions(lesson)
        self._lessons.append(lesson)

    def remove_lesson(self, lesson: Lesson) -> None:
        if lesson in self._lessons:
            self._lessons.remove(lesson)

    def get_schedule_for_group(
        self, group: AcademicGroup | str, day_of_week: int
    ) -> list[Lesson]:
        day_schedule = [
            lesson
            for lesson in self._lessons
            if (
                lesson.group == group
                or getattr(group, "number", None) == lesson.group.number
                or (isinstance(group, str) and lesson.group.number == group)
            )
            and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)

    def get_lecturer_schedule(
        self, lecturer: Lecturer | str, day_of_week: int
    ) -> list[Lesson]:
        day_schedule = [
            lesson
            for lesson in self._lessons
            if (
                lesson.lecturer == lecturer
                or getattr(lecturer, "passport_number", None)
                == lesson.lecturer.passport_number
                or getattr(lecturer, "person_id", None)
                == getattr(lesson.lecturer, "person_id", None)
                or (
                    isinstance(lecturer, str)
                    and (
                        lesson.lecturer.passport_number == lecturer
                        or getattr(lesson.lecturer, "person_id", None) == lecturer
                        or lesson.lecturer.full_name == lecturer
                    )
                )
            )
            and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)

    def get_classroom_schedule(self, room: Classroom, day_of_week: int) -> list[Lesson]:
        day_schedule = [
            lesson
            for lesson in self._lessons
            if (
                lesson.room == room
                or getattr(room, "number", None) == lesson.room.number
            )
            and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)

    def __repr__(self) -> str:
        return (
            f"Timetable(sem={self.semester_number}, lessons_count={len(self._lessons)})"
        )
