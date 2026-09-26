from lab2.domain.documents import ExpulsionOrder, ScholarshipOrder, TransferOrder
from lab2.domain.exceptions import StudentNotFoundException
from lab2.domain.grading import RecordBook
from lab2.domain.people import Dean, Student
from lab2.domain.structure import Faculty


class DeanOffice:
    """Главный фасад для управления бизнес-процессами деканата."""

    def __init__(self, faculty: Faculty, dean: Dean):
        self.faculty = faculty
        self.dean = dean
        # Реестр зачеток: ключ - person_id, значение - RecordBook
        self.record_books: dict[str, RecordBook] = {}
        # Архив всех исполненных приказов
        self._archive_orders = []

    def enroll_student(self, student: Student, group_number: str):
        """Комплексная транзакция: зачисление + выдача зачетки."""
        # 1. Строгий поиск группы (выбросит исключение, если группы нет)
        group = self.faculty.get_group_strict(group_number)

        # 2. Добавление в группу
        group.enroll_student(student)

        # 3. Автоматическое заведение зачетной книжки
        rb_number = f"ЗК-{student.record_book_number}-{group.number}"
        self.record_books[student.person_id] = RecordBook(student.person_id, rb_number)

    def get_student_record_book(self, student_id: str) -> RecordBook:
        """Поиск зачетки с защитой от пустых значений."""
        if student_id not in self.record_books:
            raise StudentNotFoundException("Зачетная книжка для данного студента не заведена.")
        return self.record_books[student_id]

    def transfer_student(self, student: Student, from_group_num: str, to_group_num: str):
        """Оформление перевода: создание приказа, подпись декана, исполнение."""
        from_group = self.faculty.get_group_strict(from_group_num)
        to_group = self.faculty.get_group_strict(to_group_num)

        # Создаем приказ (паттерн Команда)
        order = TransferOrder(student, from_group, to_group)

        # Подписываем у текущего декана ФИТиУ
        order.sign(self.dean)

        # Исполняем (физически перекладываем объект студента между списками)
        order.execute()
        self._archive_orders.append(order)

    def expel_student_for_debts(self, student: Student, reason: str = "Академическая задолженность"):
        """Комплексная процедура отчисления."""
        order = ExpulsionOrder(student, reason)
        order.sign(self.dean)
        order.execute()
        self._archive_orders.append(order)

    def summarize_session(self):
        """
        Массовая обработка результатов сессии:
        автоматическое отчисление должников и массовый приказ на стипендии отличникам.
        """
        excellent_students = []

        for group in self.faculty.groups:
            for student in group.students:
                if not student.is_active:
                    continue

                record_book = self.record_books.get(student.person_id)
                if not record_book:
                    continue

                debts = record_book.get_debts()

                # Бизнес-правило: 3 и более хвоста — на отчисление
                if len(debts) >= 3:
                    self.expel_student_for_debts(student)

                # Бизнес-правило: нет долгов и средний балл >= 8.0 — на стипендию
                elif len(debts) == 0 and record_book.average_score >= 8.0:
                    excellent_students.append(student)

        # Генерируем массовый приказ на стипендию
        if excellent_students:
            schol_order = ScholarshipOrder(excellent_students)
            schol_order.sign(self.dean)
            schol_order.execute()
            self._archive_orders.append(schol_order)

    @property
    def total_active_students(self) -> int:
        """Сводная статистика по факультету."""
        total = 0
        for group in self.faculty._groups:
            total += sum(1 for s in group._students if s.is_active)
        return total

    def get_all_debtors(self) -> list[Student]:
        """Агрегация: сквозной поиск всех академических должников на факультете."""
        debtors = []

        for group in self.faculty.groups:
            for student in group.students:
                if student.is_active:
                    rb = self.record_books.get(student.person_id)
                    if rb and len(rb.get_debts()) > 0:
                        debtors.append(student)
        return debtors

    def issue_reprimand(self, student: Student, reason: str, is_strict: bool = False):
        """Оформление дисциплинарного взыскания через Фасад."""
        from lab2.domain.documents import (
            ReprimandOrder,  # импорт можно поднять наверх файла
        )
        order = ReprimandOrder(student, reason, is_strict)
        order.sign(self.dean)
        order.execute()
        self._archive_orders.append(order)