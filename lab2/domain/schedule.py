import uuid

from lab2.domain.academics import Subject
from lab2.domain.people import Lecturer
from lab2.domain.structure import AcademicGroup


class Classroom:
    """
    Учебная аудитория.

    Attributes:
        room_id (str): Уникальный идентификатор аудитории (UUID).
        number (str): Номер аудитории (например, "412-2").
        capacity (int): Максимальная вместимость (количество посадочных мест).
        has_projector (bool): Наличие мультимедийного проектора.
        has_computers (bool): Наличие персональных компьютеров для студентов.
        is_available (bool): Доступна ли аудитория для проведения занятий (не на ремонте).
    """

    def __init__(
            self, number: str, capacity: int, has_projector: bool = False, has_computers: bool = False
    ) -> None:
        self.room_id = str(uuid.uuid4())
        self.number = number
        self.capacity = capacity
        self.has_projector = has_projector
        self.has_computers = has_computers
        self.is_available = True

    def close_for_maintenance(self) -> None:
        """Блокирует аудиторию (закрывает на ремонт)."""
        self.is_available = False

    def open_classroom(self) -> None:
        """Снимает блокировку с аудитории после завершения ремонта."""
        self.is_available = True

    def equip_with_computers(self, update_capacity_by: int = 0) -> None:
        """
        Модернизирует аудиторию в компьютерный класс.

        Args:
            update_capacity_by (int): Изменение количества мест

        Raises:
            ValueError: Если после переоборудования в аудитории не остается мест.
        """
        new_capacity = self.capacity + update_capacity_by
        if new_capacity <= 0:
            raise ValueError(
                f"Недопустимая вместимость: {new_capacity}. "
                f"Аудитория должна вмещать хотя бы одного человека."
            )

        self.has_computers = True
        self.capacity = new_capacity

    def remove_projector(self) -> None:
        """Списывает нерабочий проектор из аудитории."""
        self.has_projector = False


class Timeslot:
    """
    Временной слот для проведения занятия (пара).

    Attributes:
        sequence_number (int): Порядковый номер пары в расписании (1, 2, 3...).
        start_time (str): Время начала в формате "HH:MM".
        end_time (str): Время окончания в формате "HH:MM".
    """

    def __init__(self, sequence_number: int, start_time: str, end_time: str) -> None:
        self.sequence_number = sequence_number
        self.start_time = start_time
        self.end_time = end_time

    @property
    def duration_minutes(self) -> int:
        """Агрегация: вычисляет продолжительность занятия в минутах."""
        start_h, start_m = map(int, self.start_time.split(':'))
        end_h, end_m = map(int, self.end_time.split(':'))
        return (end_h * 60 + end_m) - (start_h * 60 + start_m)


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
        # Использование стемминга для поиска всех вариаций ("лабораторная", "лабораторные")
        if "лабораторн" in self.subject.name.lower() and not self.room.has_computers:
            raise ValueError(f"Для предмета {self.subject.name} нужна компьютерная аудитория")


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
            # Если день и номер пары совпадают, проверяем возможные пересечения ресурсов
            if existing.day_of_week == lesson.day_of_week and \
                    existing.timeslot.sequence_number == lesson.timeslot.sequence_number:

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

    def get_schedule_for_group(self, group_number: str, day_of_week: int) -> list[Lesson]:
        """
        Фильтрация: получает расписание группы на конкретный день.

        Args:
            group_number (str): Номер группы (например, "250503").
            day_of_week (int): День недели (1-7).

        Returns:
            list[Lesson]: Отсортированный по номеру пары список занятий.
        """
        day_schedule = [
            lesson for lesson in self._lessons
            if lesson.group.number == group_number and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)

    def get_lecturer_schedule(self, lecturer_id: str, day_of_week: int) -> list[Lesson]:
        """
        Фильтрация: получает расписание преподавателя на конкретный день.

        Args:
            lecturer_id (str): UUID преподавателя.
            day_of_week (int): День недели (1-7).

        Returns:
            list[Lesson]: Отсортированный по номеру пары список занятий.
        """
        day_schedule = [
            lesson for lesson in self._lessons
            if lesson.lecturer.person_id == lecturer_id and lesson.day_of_week == day_of_week
        ]
        return sorted(day_schedule, key=lambda l: l.timeslot.sequence_number)