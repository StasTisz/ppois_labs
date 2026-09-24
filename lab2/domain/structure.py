from typing import List, Optional
from lab2.domain.exceptions import DuplicateEnrollmentException, GroupNotFoundException


class Speciality:
    def __init__(self, code: str, name: str, semesters_count: int = 8):
        self.code = code
        self.name = name
        self.semesters_count = semesters_count  # Обычно 8 семестров для бакалавриата

    def __str__(self):
        return f"[{self.code}] {self.name}"

    def update_semesters_count(self, new_count: int):
        """Поведение: изменение нормативного срока обучения по специальности."""
        if not (2 <= new_count <= 12):
            raise ValueError("Недопустимое количество семестров (допустимо от 2 до 12).")
        self.semesters_count = new_count


class AcademicGroup:
    def __init__(self, number: str, speciality: Speciality, max_students: int = 30):
        self.number = number
        self.speciality = speciality
        self.max_students = max_students
        self._students = []

    @property   # геттер
    def students_count(self) -> int:
        return len(self._students)

    @property
    def students(self) -> List:
        return self._students.copy()

    def is_full(self) -> bool:
        return self.students_count >= self.max_students

    def enroll_student(self, student):
        if self.is_full():
            raise ValueError(f"Группа {self.number} переполнена. Лимит: {self.max_students}")

        if student in self._students:
            raise DuplicateEnrollmentException(f"Студент уже числится в группе {self.number}")

        self._students.append(student)

    def expel_student(self, student):
        # Если студента нет в списке, метод remove выбросит встроенный ValueError
        self._students.remove(student)

    def __str__(self):
        return f"Группа {self.number} ({self.students_count}/{self.max_students} чел.)"

    @property
    def active_students(self) -> list:
        """Возвращает список только тех студентов, кто не отчислен."""
        return [s for s in self._students if s.is_active]

    @property
    def has_vacancies(self) -> bool:
        """Проверка наличия свободных бюджетных/платных мест."""
        return self.students_count < self.max_students

    def clear_expelled(self):
        """Массовая очистка группы от отчисленных студентов (в конце года)."""
        self._students = [s for s in self._students if s.is_active]


class Department:
    def __init__(self, name: str):
        self.name = name
        self.head_name: Optional[str] = None
        self._teachers = []  # Список объектов Lecturer

    def assign_head(self, name: str):
        self.head_name = name

    def add_teacher(self, teacher):
        if teacher not in self._teachers:
            self._teachers.append(teacher)

    def remove_teacher(self, teacher):
        """Поведение: увольнение/перевод преподавателя с кафедры."""
        if teacher in self._teachers:
            self._teachers.remove(teacher)
        else:
            raise ValueError(f"Преподаватель {teacher.full_name} не числится на кафедре.")

    @property
    def staff_count(self) -> int:
        """Агрегация: количество сотрудников кафедры."""
        return len(self._teachers)


class Faculty:
    def __init__(self, name: str, short_name: str):
        self.name = name
        self.short_name = short_name
        self._departments: List[Department] = []
        self._groups: List[AcademicGroup] = []

    @property
    def groups(self) -> List[AcademicGroup]:
        return self._groups.copy()

    def add_department(self, department: Department):
        self._departments.append(department)

    def add_group(self, group: AcademicGroup):
        if self.find_group(group.number):
            raise ValueError(f"Группа {group.number} уже существует на {self.short_name}")
        self._groups.append(group)

    # Мягкий поиск
    def find_group(self, number: str) -> Optional[AcademicGroup]:
        for group in self._groups:
            if group.number == number:
                return group
        return None

    # Строгий поиск
    def get_group_strict(self, number: str) -> AcademicGroup:
        """Используется, когда мы уверены, что группа должна быть. Иначе падаем с нашей ошибкой."""
        group = self.find_group(number)
        if not group:
            raise GroupNotFoundException(f"Группа {number} не найдена на факультете {self.short_name}")
        return group

    def get_total_capacity(self) -> int:
        """Подсчет максимальной вместимости всего факультета."""
        return sum(group.max_students for group in self._groups)

    def find_student_by_id(self, person_id: str):
        """Сквозной поиск студента по всем группам факультета."""
        for group in self._groups:
            for student in group._students:
                if student.person_id == person_id:
                    return student
        return None


class University:
    def __init__(self, name: str, abbreviation: str):
        self.name = name
        self.abbreviation = abbreviation
        self._faculties: List[Faculty] = []

    def add_faculty(self, faculty: Faculty):
        if self.find_faculty(faculty.short_name):
            raise ValueError(f"Факультет '{faculty.short_name}' уже зарегистрирован в {self.abbreviation}")
        self._faculties.append(faculty)

    def find_faculty(self, short_name: str) -> Optional[Faculty]:
        for f in self._faculties:
            if f.short_name == short_name:
                return f
        return None