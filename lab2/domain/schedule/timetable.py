from __future__ import annotations

from lab2.domain.people.lecturer import Lecturer
from lab2.domain.schedule.lesson import Lesson
from lab2.domain.structure.academic_group import AcademicGroup


class Timetable:
    """
    Сводное расписание занятий на семестр.

    Attributes:
        semester_number (int): Номер текущего семестра.
    """

    def __init__(self, semester_number: int) -> None:
        self.semester_number = semester_number
        self._lessons: list[Lesson] = []

    def _validate_no_collisions(self, lesson: Lesson) -> None:
        """
        Внутренний валидатор: проверяет расписание на отсутствие накладок (коллизий).

        Args:
            lesson (Lesson): Занятие, планируемое к добавлению.

        Raises:
            ValueError: Если аудитория, преподаватель или группа уже заняты в это время.
        """
        if not lesson.room.is_available:
            raise ValueError(f"Аудитория {lesson.room.number} закрыта на ремонт")

        for existing in self._lessons:
            if existing.day_of_week == lesson.day_of_week and                     existing.timeslot.sequence_number == lesson.timeslot.sequence_number:

                if existing.room.number == lesson.room.number:
                    raise ValueError(f"Накладка: аудитория {lesson.room.number} уже занята")

                if existing.group.number == lesson.group.number:
                    raise ValueError(f"Накладка: у группы {lesson.group.number} уже есть пара в это время")

                if existing.lecturer.person_id == lesson.lecturer.person_id:
                    raise ValueError(f"Накладка: преподаватель {lesson.lecturer.full_name} уже ведет пару")

    def add_lesson(self, lesson: Lesson) -> None:
        """
        Добавляет новое занятие в расписание.

        Args:
            lesson (Lesson): Подготовленный объект занятия.
        """
        self._validate_no_collisions(lesson)
        self._lessons.append(lesson)

    def get_schedule_for_group(self, group: AcademicGroup | str, day_of_week: int) -> list[Lesson]:
        """
        Фильтрация: получает расписание группы на конкретный день.

        Args:
            group (AcademicGroup | str): Экземпляр группы или номер группы (например, "250503").
            day_of_week (int): День недели (1-7).

        Returns:
            list[Lesson]: Отсортированный по номеру пары список занятий.
        """
        group_num = group.number if isinstance(group, AcademicGroup) else group
        day_schedule = [
            lesson for lesson in self._lessons
            if lesson.group.number == group_num and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)

    def get_lecturer_schedule(self, lecturer: Lecturer | str, day_of_week: int) -> list[Lesson]:
        """
        Фильтрация: получает расписание преподавателя на конкретный день.

        Args:
            lecturer (Lecturer | str): Экземпляр преподавателя или его UUID.
            day_of_week (int): День недели (1-7).

        Returns:
            list[Lesson]: Отсортированный по номеру пары список занятий.
        """
        lecturer_id = lecturer.person_id if isinstance(lecturer, Lecturer) else lecturer
        day_schedule = [
            lesson for lesson in self._lessons
            if lesson.lecturer.person_id == lecturer_id and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)
