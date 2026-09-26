from lab2.domain.documents import (
    Document,
    ExpulsionOrder,
    ReprimandOrder,
    ScholarshipOrder,
    TransferOrder,
)
from lab2.domain.exceptions import StudentNotFoundException
from lab2.domain.grading import RecordBook
from lab2.domain.people import Dean, Student
from lab2.domain.structure import Faculty


class DeanOffice:
    """
    Главный фасад для управления бизнес-процессами деканата (например, ФИТиУ).
    Скрывает сложность подсистем, предоставляя удобный высокоуровневый интерфейс.

    Attributes:
        faculty (Faculty): Управляемый факультет.
        dean (Dean): Декан, уполномоченный подписывать документы.
        record_books (dict[str, RecordBook]): Реестр зачетных книжек (ключ - UUID студента).
    """
    MAX_ALLOWED_DEBTS = 3
    MIN_SCHOLARSHIP_SCORE = 8.0

    def __init__(self, faculty: Faculty, dean: Dean) -> None:
        self.faculty = faculty
        self.dean = dean
        self.record_books: dict[str, RecordBook] = {}
        self._archive_orders: list[Document] = []

    def _process_order(self, order: Document) -> None:
        """
        Автоматизирует жизненный цикл любого приказа.
        Подписывает у декана, пускает в исполнение и сохраняет в архив.

        Args:
            order (Document): Подготовленный проект приказа.
        """
        order.sign(self.dean)
        order.execute()
        self._archive_orders.append(order)

    def enroll_student(self, student: Student, group_number: str) -> None:
        """
        Комплексная транзакция: зачисление в группу и автоматическая выдача зачетки.

        Args:
            student (Student): Абитуриент для зачисления.
            group_number (str): Номер целевой группы.
        """
        # 1. Строгий поиск группы (выбросит исключение, если группы нет)
        group = self.faculty.get_group_strict(group_number)

        # 2. Добавление в группу
        group.enroll_student(student)

        # 3. Автоматическое заведение зачетной книжки
        rb_number = f"ЗК-{student.record_book_number}-{group.number}"
        self.record_books[student.person_id] = RecordBook(student.person_id, rb_number)

    def get_student_record_book(self, student_id: str) -> RecordBook:
        """
        Безопасный поиск зачетной книжки по идентификатору студента.

        Args:
            student_id (str): UUID студента.

        Returns:
            RecordBook: Объект зачетной книжки.

        Raises:
            StudentNotFoundException: Если зачетка не заведена.
        """
        if student_id not in self.record_books:
            raise StudentNotFoundException("Зачетная книжка для данного студента не заведена.")
        return self.record_books[student_id]

    def transfer_student(self, student: Student, from_group_num: str, to_group_num: str) -> None:
        """
        Оформление перевода студента между группами через официальный приказ.

        Args:
            student (Student): Переводимый студент.
            from_group_num (str): Номер исходной группы.
            to_group_num (str): Номер целевой группы.
        """
        from_group = self.faculty.get_group_strict(from_group_num)
        to_group = self.faculty.get_group_strict(to_group_num)

        order = TransferOrder(student, from_group, to_group)
        self._process_order(order)

    def expel_student_for_debts(
            self, student: Student, reason: str = "Академическая задолженность") -> None:
        """Оформляет отчисление студента и применяет приказ."""
        order = ExpulsionOrder(student, reason)
        self._process_order(order)

    def issue_reprimand(self, student: Student, reason: str, is_strict: bool = False) -> None:
        """Оформление дисциплинарного взыскания (выговора)."""
        order = ReprimandOrder(student, reason, is_strict)
        self._process_order(order)

    def summarize_session(self) -> None:
        """
        Массовая обработка результатов сессии:
        автоматическое отчисление злостных должников и назначение стипендий отличникам.
        """
        excellent_students: list[Student] = []

        for group in self.faculty.groups:
            for student in group.students:
                if not student.is_active:
                    continue

                record_book = self.record_books.get(student.person_id)
                if not record_book:
                    continue

                debts = record_book.get_debts()

                # Отчисление при превышении лимита долгов
                if len(debts) >= self.MAX_ALLOWED_DEBTS:
                    self.expel_student_for_debts(student)

                # Стипендия при отсутствии долгов и высоком среднем балле
                elif len(debts) == 0 and record_book.average_score >= self.MIN_SCHOLARSHIP_SCORE:
                    excellent_students.append(student)

        # Генерируем массовый приказ на стипендию одной транзакцией
        if excellent_students:
            schol_order = ScholarshipOrder(excellent_students)
            self._process_order(schol_order)

    @property
    def total_active_students(self) -> int:
        """Агрегация: подсчет всех активных студентов на факультете."""
        total = 0
        for group in self.faculty.groups:
            total += sum(1 for student in group.students if student.is_active)
        return total

    def get_all_debtors(self) -> list[Student]:
        """Агрегация: сквозной поиск всех академических должников на факультете."""
        debtors: list[Student] = []

        for group in self.faculty.groups:
            for student in group.students:
                if not student.is_active:
                    continue

                rb = self.record_books.get(student.person_id)
                if rb and len(rb.get_debts()) > 0:
                    debtors.append(student)

        return debtors