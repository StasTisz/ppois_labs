from typing import List, Optional
from lab2.domain.exceptions import DuplicateEnrollmentException, GroupNotFoundException


class Speciality:
    def __init__(self, code: str, name: str, semesters_count: int = 8):
        self.code = code
        self.name = name
        self.semesters_count = semesters_count  # Обычно 8 семестров для бакалавриата

    def __str__(self):
        return f"[{self.code}] {self.name}"


class AcademicGroup:
    def __init__(self, number: str, speciality: Speciality, max_students: int = 30):
        self.number = number
        self.speciality = speciality
        self.max_students = max_students
        self._students = []

    @property   # геттер
    def students_count(self) -> int:
        return len(self._students)

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

#     Кафедра
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


class Faculty:
    def __init__(self, name: str, short_name: str):
        self.name = name
        self.short_name = short_name
        self._departments: List[Department] = []
        self._groups: List[AcademicGroup] = []

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