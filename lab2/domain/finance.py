import uuid
from datetime import datetime, timezone

from lab2.domain.people import Employee, Student


class BankAccount:
    """
    Счет студента или сотрудника для начислений и оплат.

    Attributes:
        account_id (str): Уникальный внутренний идентификатор (UUID).
        owner_id (str): Идентификатор владельца (Student.person_id или Employee.person_id).
        account_number (str): Уникальный банковский номер счета.
        balance (float): Текущий баланс.
        is_blocked (bool): Статус блокировки счета.
    """

    def __init__(self, owner_id: str, account_number: str) -> None:
        self.account_id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.account_number = account_number
        self.balance = 0.0
        self.is_blocked = False

    def deposit(self, amount: float) -> None:
        """
        Пополняет счет на указанную сумму.

        Args:
            amount (float): Сумма пополнения.

        Raises:
            ValueError: Если сумма нулевая или отрицательная.
        """
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Списывает средства со счета с проверкой блокировки и баланса.

        Args:
            amount (float): Сумма списания.

        Raises:
            ValueError: Если счет заблокирован, сумма <= 0 или недостаточно средств.
        """
        if self.is_blocked:
            raise ValueError("Операция отклонена: счет заблокирован")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля")
        if self.balance < amount:
            raise ValueError(f"Недостаточно средств. Баланс: {self.balance}")
        self.balance -= amount

    def block_account(self) -> None:
        """Блокирует счет от любых расходных операций."""
        self.is_blocked = True

    def transfer_to(self, target_account: 'BankAccount', amount: float) -> None:
        """
        Выполняет перевод средств на другой счет (транзакция).

        Args:
            target_account (BankAccount): Счет получателя.
            amount (float): Сумма перевода.

        Raises:
            ValueError: При попытке перевести деньги самому себе.
        """
        if self.account_id == target_account.account_id:
            raise ValueError("Нельзя перевести деньги самому себе.")

        # Метод withdraw уже содержит необходимые защитные проверки
        self.withdraw(amount)
        target_account.deposit(amount)


class TuitionContract:
    """
    Договор на платное обучение студента.

    Attributes:
        contract_id (str): Внутренний идентификатор договора (UUID).
        number (str): Регистрационный номер договора.
        student (Student): Студент-заказчик.
        total_amount (float): Полная стоимость обучения.
        paid_amount (float): Внесенная сумма.
        is_signed (bool): Статус подписания договора.
        creation_date (datetime): Точная дата и время создания (в UTC).
    """
    MIN_DISCOUNT_PERCENT = 0.0
    MAX_DISCOUNT_PERCENT = 100.0
    OVERDUE_RATIO = 0.5  # Порог оплаты для признания просрочки (50%)

    def __init__(self, number: str, student: Student, total_amount: float) -> None:
        self.contract_id = str(uuid.uuid4())
        self.number = number
        self.student = student
        self.total_amount = total_amount
        self.paid_amount = 0.0
        self.is_signed = False
        self.creation_date = datetime.now(timezone.utc)

    def _sync_student_debt(self) -> None:
        """Внутренний помощник: синхронизирует задолженность с профилем студента."""
        self.student.financial_debt = self.debt

    def sign_contract(self) -> None:
        """Утверждает договор и фиксирует финансовую задолженность за студентом."""
        self.is_signed = True
        self._sync_student_debt()

    @property
    def debt(self) -> float:
        """Агрегация: вычисляет текущий остаток неоплаченного долга."""
        return self.total_amount - self.paid_amount

    @property
    def is_fully_paid(self) -> bool:
        """Бизнес-правило: проверяет, погашена ли задолженность полностью."""
        return self.debt <= 0

    def pay_tuition(self, amount: float, account: BankAccount) -> None:
        """
        Оплачивает обучение путем безналичного списания со счета.

        Args:
            amount (float): Сумма платежа.
            account (BankAccount): Банковский счет, с которого списываются средства.

        Raises:
            ValueError: Если договор еще не подписан.
        """
        if not self.is_signed:
            raise ValueError("Нельзя оплатить неподписанный договор")

        account.withdraw(amount)
        self.paid_amount += amount
        self._sync_student_debt()

    def apply_discount(self, percent: float) -> None:
        """
        Применяет скидку на общую стоимость обучения.

        Args:
            percent (float): Размер скидки в процентах (от 0 до 100).

        Raises:
            ValueError: Если процент выходит за допустимые границы.
        """
        if not (self.MIN_DISCOUNT_PERCENT < percent <= self.MAX_DISCOUNT_PERCENT):
            raise ValueError(
                f"Процент скидки должен быть от {self.MIN_DISCOUNT_PERCENT} до {self.MAX_DISCOUNT_PERCENT}."
            )
        discount_amount = self.total_amount * (percent / 100)
        self.total_amount -= discount_amount
        self._sync_student_debt()

    @property
    def is_overdue(self) -> bool:
        """
        Бизнес-правило: проверяет, является ли платеж просроченным.
        Просрочка фиксируется, если внесено менее установленного порога (50% по умолчанию).
        """
        min_required_payment = self.total_amount * self.OVERDUE_RATIO
        return self.paid_amount < min_required_payment


class Payroll:
    """
    Зарплатная ведомость и стипендиальный фонд для массовых выплат.

    Attributes:
        month (int): Месяц выплат.
        year (int): Год выплат.
        total_fund (float): Общая сумма выданных средств.
    """
    DEFAULT_SCHOLARSHIP = 120.0

    def __init__(self, month: int, year: int) -> None:
        self.month = month
        self.year = year
        self.total_fund = 0.0
        self._processed_payments: list[str] = []

    def pay_salary(self, employee: Employee, account: BankAccount, bonus: float = 0.0) -> None:
        """
        Выплачивает заработную плату сотруднику (включая премии).

        Args:
            employee (Employee): Получатель выплаты.
            account (BankAccount): Счет для зачисления.
            bonus (float): Дополнительная премия.
        """
        amount = employee.salary + bonus
        account.deposit(amount)
        self.total_fund += amount
        self._processed_payments.append(f"Выплачено {amount} сотруднику {employee.full_name}")

    def pay_scholarship(
            self, student: Student, account: BankAccount, base_amount: float = DEFAULT_SCHOLARSHIP
    ) -> None:
        """
        Выплачивает стипендию активному студенту без долгов.

        Args:
            student (Student): Получатель стипендии.
            account (BankAccount): Счет для зачисления.
            base_amount (float): Базовый размер выплаты.

        Raises:
            ValueError: Если студент лишен академической стипендии.
        """
        if not student.has_scholarship:
            raise ValueError(f"Студенту {student.full_name} не назначена стипендия")

        account.deposit(base_amount)
        self.total_fund += base_amount
        self._processed_payments.append(f"Стипендия {base_amount} студенту {student.full_name}")

    @property
    def total_payments_count(self) -> int:
        """Агрегация: вычисляет общее количество проведенных транзакций фонда."""
        return len(self._processed_payments)

    def get_payment_history(self) -> list[str]:
        """
        Возвращает защищенную копию выписки по ведомости.

        Returns:
            list[str]: Массив логов с историей транзакций.
        """
        return self._processed_payments.copy()