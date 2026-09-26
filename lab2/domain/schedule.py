import uuid

from lab2.domain.academics import Subject
from lab2.domain.people import Lecturer
from lab2.domain.structure import AcademicGroup


class Classroom:
    """Учебная аудитория."""

    def __init__(self, number: str, capacity: int, has_projector: bool = False, has_computers: bool = False):
        self.room_id = str(uuid.uuid4())
        self.number = number
        self.capacity = capacity
        self.has_projector = has_projector
        self.has_computers = has_computers
        self.is_available = True

    def close_for_maintenance(self):
        """Закрыть на ремонт."""
        self.is_available = False

    def open_classroom(self):
        """Открыть после ремонта."""
        self.is_available = True

    def equip_with_computers(self, update_capacity_by: int = 0):
        """Поведение: модернизация аудитории в компьютерный класс."""
        self.has_computers = True
        if update_capacity_by > 0:
            self.capacity += update_capacity_by

    def remove_projector(self):
        """Поведение: списание нерабочего проектора из аудитории."""
        self.has_projector = False


class Timeslot:
    """Пара (временной слот)."""

    def __init__(self, sequence_number: int, start_time: str, end_time: str):
        self.sequence_number = sequence_number  # 1 (первая пара), 2 и т.д.
        self.start_time = start_time
        self.end_time = end_time

    @property
    def duration_minutes(self) -> int:
        """Пример вычисляемого свойства для чеклиста."""
        start_h, start_m = map(int, self.start_time.split(':'))
        end_h, end_m = map(int, self.end_time.split(':'))
        return (end_h * 60 + end_m) - (start_h * 60 + start_m)


class Lesson:
    """Конкретное занятие в расписании."""

    def __init__(self, subject: Subject, lecturer: Lecturer, group: AcademicGroup, room: Classroom, timeslot: Timeslot,
                 day_of_week: int):
        self.lesson_id = str(uuid.uuid4())
        self.subject = subject  # Ассоциация 1
        self.lecturer = lecturer  # Ассоциация 2
        self.group = group  # Ассоциация 3
        self.room = room  # Ассоциация 4
        self.timeslot = timeslot  # Ассоциация 5
        self.day_of_week = day_of_week  # 1 - ПН, ..., 7 - ВС

        self._validate_capacity()
        self._validate_room_equipment()

    def _validate_capacity(self):
        """Поведение: проверка вместимости аудитории."""
        if self.group.students_count > self.room.capacity:
            raise ValueError(
                f"Аудитория {self.room.number} ({self.room.capacity} мест) мала для группы {self.group.number} ({self.group.students_count} чел.)")

    def _validate_room_equipment(self):
        """Поведение: для лаб нужны компьютеры."""
        if "лабораторн" in self.subject.name.lower() and not self.room.has_computers:
            raise ValueError(f"Для предмета {self.subject.name} нужна компьютерная аудитория")


class Timetable:
    """Расписание занятий на семестр."""

    def __init__(self, semester_number: int):
        self.semester_number = semester_number
        self._lessons: list[Lesson] = []

    def add_lesson(self, lesson: Lesson):
        """Добавление занятия с защитой от накладок (коллизий)."""
        if not lesson.room.is_available:
            raise ValueError(f"Аудитория {lesson.room.number} закрыта на ремонт")

        for existing in self._lessons:
            if existing.day_of_week == lesson.day_of_week and existing.timeslot.sequence_number == lesson.timeslot.sequence_number:
                if existing.room.number == lesson.room.number:
                    raise ValueError(f"Накладка: аудитория {lesson.room.number} уже занята")
                if existing.group.number == lesson.group.number:
                    raise ValueError(f"Накладка: у группы {lesson.group.number} уже есть пара в это время")
                if existing.lecturer.person_id == lesson.lecturer.person_id:
                    raise ValueError(f"Накладка: преподаватель {lesson.lecturer.full_name} уже ведет пару")

        self._lessons.append(lesson)

    def get_schedule_for_group(self, group_number: str, day_of_week: int) -> list[Lesson]:
        """Мягкий поиск занятий группы на конкретный день."""
        day_schedule = [lesson for lesson in self._lessons if
                        lesson.group.number == group_number and lesson.day_of_week == day_of_week]
        # Сортируем по номеру пары
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)

    def get_lecturer_schedule(self, lecturer_id: str, day_of_week: int) -> list:
        """Фильтрация: получение расписания конкретного преподавателя на день."""
        day_schedule = [lesson for lesson in self._lessons if
                        lesson.lecturer.person_id == lecturer_id and lesson.day_of_week == day_of_week]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)