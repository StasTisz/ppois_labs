from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.people.lecturer import Lecturer
    from lab2.domain.schedule.classroom import Classroom
    from lab2.domain.schedule.timeslot import Timeslot
    from lab2.domain.structure.academic_group import AcademicGroup


class Lesson:
    def __init__(
        self,
        subject: Subject,
        lecturer: Lecturer,
        group: AcademicGroup,
        room: Classroom,
        timeslot: Timeslot,
        day_of_week: int,
    ) -> None:
        self.subject = subject
        self.lecturer = lecturer
        self.group = group
        self.room = room
        self.timeslot = timeslot
        self.day_of_week = day_of_week
        self._validate_capacity()
        self._validate_room_equipment()

    def _validate_capacity(self) -> None:
        if self.group.students_count > self.room.capacity:
            raise ValueError(
                f"Аудитория {self.room.number} ({self.room.capacity} мест) мала "
                f"для группы {self.group.number} ({self.group.students_count} чел.)"
            )

    def _validate_room_equipment(self) -> None:
        if "лабораторн" in self.subject.name.lower() and not self.room.has_computers:
            raise ValueError(
                f"Для предмета {self.subject.name} нужна компьютерная аудитория"
            )

    def change_room(self, new_room: Classroom) -> None:
        old_room = self.room
        self.room = new_room
        try:
            self._validate_capacity()
            self._validate_room_equipment()
        except ValueError:
            self.room = old_room
            raise

    def change_timeslot(self, new_slot: Timeslot, day_of_week: int) -> None:
        if not (1 <= day_of_week <= 7):
            raise ValueError(f"Недопустимый день недели: {day_of_week}.")
        self.timeslot = new_slot
        self.day_of_week = day_of_week

    def reschedule(
        self, new_room: Classroom, new_slot: Timeslot, day_of_week: int
    ) -> None:
        self.change_room(new_room)
        self.change_timeslot(new_slot, day_of_week)

    def __repr__(self) -> str:
        return (
            f"Lesson(subj={self.subject.name!r}, group={self.group.number!r}, "
            f"room={self.room.number!r}, day={self.day_of_week}, slot={self.timeslot.sequence_number})"
        )
