from typing import List, Optional, Any
from lab2.domain.exceptions import DuplicateEnrollmentException, GroupNotFoundException


class Speciality:
    """
    Учебная специальность университета.

    Attributes:
        code (str): Шифр специальности (например, "1-40 05 01").
        name (str): Полное наименование специальности.
        semesters_count (int): Нормативный срок обучения в семестрах.
    """
    DEFAULT_SEMESTERS = 8
    MIN_SEMESTERS = 2
    MAX_SEMESTERS = 12

    def __init__(self, code: str, name: str, semesters_count: int = DEFAULT_SEMESTERS) -> None:
        self.code = code
        self.name = name
        self.semesters_count = semesters_count

    def __str__(self) -> str:
        return f"[{self.code}] {self.name}"

    def update_semesters_count(self, new_count: int) -> None:
        """
        Изменяет нормативный срок обучения по специальности.

        Args:
            new_count (int): Новое количество семестров.

        Raises:
            ValueError: Если количество семестров выходит за допустимые границы.
        """
        if not (self.MIN_SEMESTERS <= new_count <= self.MAX_SEMESTERS):
            raise ValueError(
                f"Недопустимое количество семестров. "
                f"Допустимо от {self.MIN_SEMESTERS} до {self.MAX_SEMESTERS}."
            )
        self.semesters_count = new_count


class AcademicGroup:
    """
    Академическая учебная группа студентов.

    Attributes:
        number (str): Номер группы (например, "521702").
        speciality (Speciality): Специальность, к которой прикреплена группа.
        max_students (int): Максимально допустимое количество студентов.
    """
    DEFAULT_MAX_STUDENTS = 30

    def __init__(self, number: str, speciality: Speciality, max_students: int = DEFAULT_MAX_STUDENTS) -> None:
        self.number = number
        self.speciality = speciality
        self.max_students = max_students
        self._students: List[Any] = []  # Ожидаются объекты класса Student

    @property
    def students_count(self) -> int:
        """Возвращает текущее количество студентов в группе."""
        return len(self._students)

    @property
    def students(self) -> List[Any]:
        """Возвращает защищенную копию списка студентов."""
        return self._students.copy()

    @property
    def active_students(self) -> List[Any]:
        """Возвращает список только тех студентов, кто не отчислен."""
        return [s for s in self._students if s.is_active]

    @property
    def has_vacancies(self) -> bool:
        """Проверка наличия свободных мест в группе."""
        return self.students_count < self.max_students

    def is_full(self) -> bool:
        """Проверяет, достигнут ли лимит вместимости группы."""
        return not self.has_vacancies

    def enroll_student(self, student: Any) -> None:
        """
        Зачисляет студента в группу.

        Args:
            student: Объект зачисляемого студента.

        Raises:
            ValueError: Если группа переполнена.
            DuplicateEnrollmentException: Если студент уже числится в этой группе.
        """
        if self.is_full():
            raise ValueError(f"Группа {self.number} переполнена. Лимит: {self.max_students}")

        if student in self._students:
            raise DuplicateEnrollmentException(f"Студент уже числится в группе {self.number}")

        self._students.append(student)

    def expel_student(self, student: Any) -> None:
        """
        Исключает студента из списка группы.

        Args:
            student: Объект отчисляемого студента.

        Raises:
            ValueError: Если студент не найден в группе (выбрасывается встроенным методом list.remove).
        """
        self._students.remove(student)

    def clear_expelled(self) -> None:
        """Массовая очистка группы от отчисленных студентов (вызывается при подведении итогов)."""
        self._students = self.active_students

    def __str__(self) -> str:
        return f"Группа {self.number} ({self.students_count}/{self.max_students} чел.)"


class Department:
    """
    Учебная кафедра факультета.

    Attributes:
        name (str): Название кафедры.
        head_name (Optional[str]): ФИО заведующего кафедрой.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.head_name: Optional[str] = None
        self._teachers: List[Any] = []  # Ожидаются объекты класса Lecturer

    @property
    def staff_count(self) -> int:
        """Агрегация: текущее количество сотрудников кафедры."""
        return len(self._teachers)

    def assign_head(self, name: str) -> None:
        """Назначает заведующего кафедрой."""
        self.head_name = name

    def add_teacher(self, teacher: Any) -> None:
        """
        Нанимает преподавателя на кафедру.

        Args:
            teacher: Объект преподавателя.
        """
        if teacher not in self._teachers:
            self._teachers.append(teacher)

    def remove_teacher(self, teacher: Any) -> None:
        """
        Увольняет или переводит преподавателя с кафедры.

        Args:
            teacher: Объект преподавателя.

        Raises:
            ValueError: Если преподаватель не числится на кафедре.
        """
        if teacher in self._teachers:
            self._teachers.remove(teacher)
        else:
            # Предполагается, что у teacher есть свойство full_name
            name = getattr(teacher, 'full_name', str(teacher))
            raise ValueError(f"Преподаватель {name} не числится на кафедре {self.name}.")


class Faculty:
    """
    Учебный факультет университета.

    Attributes:
        name (str): Полное название факультета.
        short_name (str): Аббревиатура факультета (например, "ФИТиУ").
    """
    def __init__(self, name: str, short_name: str) -> None:
        self.name = name
        self.short_name = short_name
        self._departments: List[Department] = []
        self._groups: List[AcademicGroup] = []

    @property
    def groups(self) -> List[AcademicGroup]:
        """Возвращает защищенную копию списка групп."""
        return self._groups.copy()

    def add_department(self, department: Department) -> None:
        """Прикрепляет кафедру к факультету."""
        self._departments.append(department)

    def add_group(self, group: AcademicGroup) -> None:
        """
        Регистрирует новую академическую группу на факультете.

        Args:
            group: Объект добавляемой группы.

        Raises:
            ValueError: Если группа с таким номером уже существует.
        """
        if self.find_group(group.number):
            raise ValueError(f"Группа {group.number} уже существует на {self.short_name}")
        self._groups.append(group)

    def find_group(self, number: str) -> Optional[AcademicGroup]:
        """
        Мягкий поиск группы по номеру (возвращает None, если не найдена).
        """
        for group in self._groups:
            if group.number == number:
                return group
        return None

    def get_group_strict(self, number: str) -> AcademicGroup:
        """
        Строгий поиск группы по номеру (для бизнес-логики, требующей гарантии существования).

        Raises:
            GroupNotFoundException: Если группа не найдена.
        """
        group = self.find_group(number)
        if not group:
            raise GroupNotFoundException(f"Группа {number} не найдена на факультете {self.short_name}")
        return group

    def get_total_capacity(self) -> int:
        """Подсчитывает максимальную суммарную вместимость всех групп факультета."""
        return sum(group.max_students for group in self._groups)

    def find_student_by_id(self, person_id: str) -> Optional[Any]:
        """
        Сквозной поиск студента по номеру билета/идентификатору среди всех групп факультета.
        """
        for group in self._groups:
            # Прямое обращение к защищенному полю _students допустимо только если
            # мы инкапсулируем эту логику внутри домена, но лучше использовать .students
            for student in group.students:
                if getattr(student, 'person_id', None) == person_id:
                    return student
        return None


class University:
    """
    Университет как корневая структура предметной области.

    Attributes:
        name (str): Полное название учебного заведения.
        abbreviation (str): Краткая аббревиатура.
    """
    def __init__(self, name: str, abbreviation: str) -> None:
        self.name = name
        self.abbreviation = abbreviation
        self._faculties: List[Faculty] = []

    def add_faculty(self, faculty: Faculty) -> None:
        """
        Регистрирует новый факультет.

        Raises:
            ValueError: Если факультет с такой аббревиатурой уже существует.
        """
        if self.find_faculty(faculty.short_name):
            raise ValueError(f"Факультет '{faculty.short_name}' уже зарегистрирован в {self.abbreviation}")
        self._faculties.append(faculty)

    def find_faculty(self, short_name: str) -> Optional[Faculty]:
        """Ищет факультет по аббревиатуре."""
        for f in self._faculties:
            if f.short_name == short_name:
                return f
        return None