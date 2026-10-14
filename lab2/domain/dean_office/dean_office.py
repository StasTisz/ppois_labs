from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.documents.expulsion_order import ExpulsionOrder
from lab2.domain.documents.reprimand_order import ReprimandOrder
from lab2.domain.documents.scholarship_order import ScholarshipOrder
from lab2.domain.documents.transfer_order import TransferOrder
from lab2.domain.exceptions import StudentNotFoundException
from lab2.domain.grading.record_book import RecordBook
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.faculty import Faculty

ExecutableOrder = ExpulsionOrder | ReprimandOrder | ScholarshipOrder | TransferOrder


class DeanOffice:
    MAX_ALLOWED_DEBTS = 3
    MIN_SCHOLARSHIP_SCORE = 8.0

    def __init__(self, faculty: Faculty, dean: Dean) -> None:
        self.faculty = faculty
        self.dean = dean
        self._record_books: dict[Student, RecordBook] = {}
        self._archive_orders: list[Document] = []

    @property
    def archive_orders(self) -> list[Document]:
        return list(self._archive_orders)

    def _process_order(self, order: ExecutableOrder) -> None:
        order.sign(self.dean)
        order.execute()
        self._archive_orders.append(order)

    def enroll_student(self, student: Student, group: AcademicGroup) -> None:
        group.enroll_student(student)
        rb_number = f"ЗК-{student.record_book_number}-{group.number}"
        rb = RecordBook(student, rb_number)
        student.record_book = rb
        self._record_books[student] = rb

    def get_student_record_book(self, student: Student) -> RecordBook:
        if student.record_book is not None:
            return student.record_book
        if student in self._record_books:
            return self._record_books[student]
        raise StudentNotFoundException(
            f"Зачетная книжка для студента {student.full_name} не заведена."
        )

    def transfer_student(
        self,
        student: Student,
        from_group: AcademicGroup,
        to_group: AcademicGroup,
    ) -> None:
        order = TransferOrder(student, from_group, to_group)
        self._process_order(order)

    def expel_student_for_debts(
        self, student: Student, reason: str = "Академическая задолженность"
    ) -> None:
        order = ExpulsionOrder(student, reason)
        self._process_order(order)

    def issue_reprimand(
        self, student: Student, reason: str, is_strict: bool = False
    ) -> None:
        order = ReprimandOrder(student, reason, is_strict)
        self._process_order(order)

    def _evaluate_student_session(
        self, student: Student, excellent_students: list[Student]
    ) -> None:
        if not student.is_active:
            return
        record_book = student.record_book or self._record_books.get(student)
        if not record_book:
            return
        debts = record_book.get_debts()
        if len(debts) >= self.MAX_ALLOWED_DEBTS:
            self.expel_student_for_debts(student)
        elif len(debts) == 0 and record_book.average_score >= self.MIN_SCHOLARSHIP_SCORE:
            excellent_students.append(student)

    def summarize_session(self) -> None:
        excellent_students: list[Student] = []
        for group in self.faculty.groups:
            for student in group.students:
                self._evaluate_student_session(student, excellent_students)

        if excellent_students:
            schol_order = ScholarshipOrder(excellent_students)
            self._process_order(schol_order)

    def _is_debtor(self, student: Student) -> bool:
        if not student.is_active:
            return False
        rb = student.record_book or self._record_books.get(student)
        return bool(rb and len(rb.get_debts()) > 0)

    def get_all_debtors(self) -> list[Student]:
        debtors: list[Student] = []
        for group in self.faculty.groups:
            debtors.extend(s for s in group.students if self._is_debtor(s))
        return debtors

    @property
    def total_active_students(self) -> int:
        return sum(
            sum(1 for s in group.students if s.is_active)
            for group in self.faculty.groups
        )
