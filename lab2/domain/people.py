import uuid
from typing import List


class Person:
    def __init__(self, first_name: str, last_name: str, middle_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.person_id = str(uuid.uuid4())  # Уникальный UUID, чтобы различать однофамильцев

    @property
    def full_name(self) -> str:
        if self.middle_name:    # У человека может не быть отчества
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.full_name

    def change_last_name(self, new_last_name: str):
        """Поведение: смена фамилии (например, при вступлении в брак)."""
        if not new_last_name.strip():
            raise ValueError("Фамилия не может быть пустой.")
        self.last_name = new_last_name


class Student(Person):
    def __init__(self, first_name: str, last_name: str, middle_name: str = "", record_book_number: str = ""):
        super().__init__(first_name, last_name, middle_name)

        self.record_book_number = record_book_number
        self.is_active = True  # False, если отчислен или в академе
        self.has_scholarship = False
        self.financial_debt = 0.0  # Долг за платное обучение или общежитие

    def expel(self):
        # Жестко меняет статус студента. Отсюда идет удаление из AcademicGroup
        self.is_active = False
        self.has_scholarship = False

    def grant_scholarship(self):
        if not self.is_active:
            raise ValueError(f"Нельзя назначить стипендию отчисленному студенту {self.full_name}")
        self.has_scholarship = True

    @property
    def is_debtor(self) -> bool:
        """Бизнес-свойство: является ли студент финансовым должником."""
        return self.financial_debt > 0.0

    def pay_debt(self, amount: float):
        """Частичное или полное погашение долга студентом."""
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной.")
        if amount > self.financial_debt:
            self.financial_debt = 0.0
        else:
            self.financial_debt -= amount


class Employee(Person):
    def __init__(self, first_name: str, last_name: str, middle_name: str = "", position: str = ""):
        super().__init__(first_name, last_name, middle_name)
        self.position = position
        self.salary = 0.0

    def promote(self, new_position: str, salary_increase: float = 0.0):
        """Поведение: повышение сотрудника в должности с изменением оклада."""
        self.position = new_position
        if salary_increase > 0:
            self.salary += salary_increase

    def change_salary(self, new_salary: float):
        """Поведение: установка нового оклада с валидацией."""
        if new_salary < 0:
            raise ValueError("Оклад не может быть отрицательным.")
        self.salary = new_salary


class Lecturer(Employee):
    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = "Без степени"):
        super().__init__(first_name, last_name, middle_name, position="Преподаватель")
        self.degree = degree
        self._subjects: List[str] = []

    def assign_subject(self, subject_name: str):
        # Защита от двойного назначения одной и той же дисциплины
        if subject_name not in self._subjects:
            self._subjects.append(subject_name)

    def update_degree(self, new_degree: str):
        if not new_degree.strip():
            raise ValueError("Ученая степень не может быть пустой строкой")
        self.degree = new_degree

    def can_teach(self, subject_name: str) -> bool:
        """Проверка компетенции преподавателя."""
        return subject_name in self._subjects

    @property
    def subjects_count(self) -> int:
        """Количество читаемых дисциплин (нагрузка)."""
        return len(self._subjects)


class Dean(Employee):
    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = "К.т.н."):
        super().__init__(first_name, last_name, middle_name, position="Декан")
        self.degree = degree

    def sign_order(self, order_text: str) -> str:
        # Базовая заглушка для работы с приказами (реализуем в documents.py)
        return f"ПРИКАЗ УТВЕРЖДЕН: {order_text} | Подписант: декан {self.full_name}"


class Assistant(Lecturer):
    """Ассистент: ведет только лабораторные и практические занятия, обычно без степени."""

    def __init__(self, first_name: str, last_name: str, middle_name: str = ""):
        # Ассистенты обычно магистры
        super().__init__(first_name, last_name, middle_name, degree="Магистр")


class AssociateProfessor(Lecturer):
    """Доцент: читает лекционные курсы, имеет ученую степень."""

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = "К.т.н."):
        super().__init__(first_name, last_name, middle_name, degree=degree)


class Professor(Lecturer):
    """Профессор: высший академический статус на кафедре."""

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = "Д.т.н."):
        super().__init__(first_name, last_name, middle_name, degree=degree)