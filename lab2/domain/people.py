import uuid


class Person:
    """
    Базовый класс для всех физических лиц в предметной области университета.

    Attributes:
        first_name (str): Имя.
        last_name (str): Фамилия.
        middle_name (str): Отчество (может быть пустым).
        person_id (str): Уникальный внутренний идентификатор (UUID).
    """

    def __init__(self, first_name: str, last_name: str, middle_name: str = "") -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.person_id = str(uuid.uuid4())

    @property
    def full_name(self) -> str:
        """Агрегация ФИО в единую строку с учетом возможного отсутствия отчества."""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    def __str__(self) -> str:
        return self.full_name

    def change_last_name(self, new_last_name: str) -> None:
        """
        Изменяет фамилию человека (например, при вступлении в брак).

        Args:
            new_last_name (str): Новая фамилия.

        Raises:
            ValueError: Если передана пустая строка.
        """
        if not new_last_name.strip():
            raise ValueError("Фамилия не может быть пустой.")
        self.last_name = new_last_name


class Student(Person):
    """
    Студент университета.

    Attributes:
        record_book_number (str): Номер зачетной книжки.
        is_active (bool): Статус обучения (False, если отчислен или в академе).
        has_scholarship (bool): Наличие академической стипендии.
        financial_debt (float): Текущий долг за платное обучение или общежитие.
    """

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", record_book_number: str = "") -> None:
        super().__init__(first_name, last_name, middle_name)
        self.record_book_number = record_book_number
        self.is_active = True
        self.has_scholarship = False
        self.financial_debt = 0.0

    def expel(self) -> None:
        """Отчисляет студента, деактивируя его статус и лишая стипендии."""
        self.is_active = False
        self.has_scholarship = False

    def grant_scholarship(self) -> None:
        """
        Назначает академическую стипендию.

        Raises:
            ValueError: Если попытка назначить стипендию неактивному (отчисленному) студенту.
        """
        if not self.is_active:
            raise ValueError(f"Нельзя назначить стипендию отчисленному студенту {self.full_name}")
        self.has_scholarship = True

    @property
    def is_debtor(self) -> bool:
        """Проверяет, имеет ли студент непогашенную финансовую задолженность."""
        return self.financial_debt > 0.0

    def pay_debt(self, amount: float) -> None:
        """
        Частично или полностью погашает финансовую задолженность студента.

        Args:
            amount (float): Сумма внесенного платежа.

        Raises:
            ValueError: Если сумма платежа отрицательная или равна нулю.
        """
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной.")
        if amount > self.financial_debt:
            self.financial_debt = 0.0
        else:
            self.financial_debt -= amount


class Employee(Person):
    """
    Сотрудник университета.

    Attributes:
        position (str): Текущая должность.
        salary (float): Текущий оклад.
    """

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", position: str = "") -> None:
        super().__init__(first_name, last_name, middle_name)
        self.position = position
        self.salary = 0.0

    def promote(self, new_position: str, salary_increase: float = 0.0) -> None:
        """
        Повышает сотрудника в должности с опциональным увеличением оклада.

        Args:
            new_position (str): Название новой должности.
            salary_increase (float): Сумма прибавки к окладу (по умолчанию 0.0).
        """
        self.position = new_position
        if salary_increase > 0:
            self.salary += salary_increase

    def change_salary(self, new_salary: float) -> None:
        """
        Устанавливает новый размер оклада.

        Args:
            new_salary (float): Новый размер оклада.

        Raises:
            ValueError: Если новый оклад отрицательный.
        """
        if new_salary < 0:
            raise ValueError("Оклад не может быть отрицательным.")
        self.salary = new_salary


class Lecturer(Employee):
    """
    Преподаватель университета (базовый класс для профильных преподавателей).

    Attributes:
        degree (str): Ученая степень.
    """
    DEFAULT_DEGREE = "Без степени"
    DEFAULT_POSITION = "Преподаватель"

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, position=self.DEFAULT_POSITION)
        self.degree = degree
        self._subjects: list[str] = []

    @property
    def subjects_count(self) -> int:
        """Агрегация: количество читаемых преподавателем дисциплин."""
        return len(self._subjects)

    def assign_subject(self, subject_name: str) -> None:
        """
        Назначает преподавателю новую дисциплину для ведения.
        Защищает от дублирования одной и той же дисциплины.

        Args:
            subject_name (str): Название учебной дисциплины.
        """
        if subject_name not in self._subjects:
            self._subjects.append(subject_name)

    def update_degree(self, new_degree: str) -> None:
        """
        Обновляет ученую степень преподавателя (например, после защиты диссертации).

        Raises:
            ValueError: Если передана пустая строка.
        """
        if not new_degree.strip():
            raise ValueError("Ученая степень не может быть пустой строкой")
        self.degree = new_degree

    def can_teach(self, subject_name: str) -> bool:
        """
        Проверяет компетенцию: ведет ли преподаватель указанную дисциплину.
        """
        return subject_name in self._subjects


class Dean(Employee):
    """
    Декан факультета. Подписывает приказы и руководит факультетом.
    """
    DEFAULT_DEGREE = "К.т.н."
    DEFAULT_POSITION = "Декан"

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, position=self.DEFAULT_POSITION)
        self.degree = degree

    def sign_order(self, order_text: str) -> str:
        """
        Подписывает приказ по факультету.

        Args:
            order_text (str): Текст приказа.

        Returns:
            str: Форматированная строка подписанного приказа.
        """
        return f"ПРИКАЗ УТВЕРЖДЕН: {order_text} | Подписант: декан {self.full_name}"


class Assistant(Lecturer):
    """
    Ассистент кафедры. Обычно ведет лабораторные и практические занятия.
    """
    DEFAULT_DEGREE = "Магистр"

    def __init__(self, first_name: str, last_name: str, middle_name: str = "") -> None:
        super().__init__(first_name, last_name, middle_name, degree=self.DEFAULT_DEGREE)


class AssociateProfessor(Lecturer):
    """
    Доцент кафедры. Читает лекционные курсы, как правило, имеет степень кандидата наук.
    """
    DEFAULT_DEGREE = "К.т.н."

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, degree=degree)


class Professor(Lecturer):
    """
    Профессор кафедры. Высший академический статус, как правило, имеет степень доктора наук.
    """
    DEFAULT_DEGREE = "Д.т.н."

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, degree=degree)