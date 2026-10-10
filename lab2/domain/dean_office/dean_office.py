from __future__ import annotations

from typing import Any

from lab2.domain.documents.document import Document
from lab2.domain.documents.expulsion_order import ExpulsionOrder
from lab2.domain.documents.reprimand_order import ReprimandOrder
from lab2.domain.documents.scholarship_order import ScholarshipOrder
from lab2.domain.documents.transfer_order import TransferOrder
from lab2.domain.exceptions import StudentNotFoundException
from lab2.domain.grading.record_book import RecordBook
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student
from lab2.domain.structure.faculty import Faculty

ExecutableOrder = ExpulsionOrder | ReprimandOrder | ScholarshipOrder | TransferOrder


class DeanOffice:
    MAX_ALLOWED_DEBTS = 3
    MIN_SCHOLARSHIP_SCORE = 8.0

    def __init__(self, faculty: Faculty, dean: Dean) -> None:
        self.faculty = faculty
        self.dean = dean
        self.record_books: dict[Any, RecordBook] = {}
        self._archive_orders: list[Document] = []

    def _process_order(self, order: ExecutableOrder) -> None:
        order.sign(self.dean)
        order.execute()
        self._archive_orders.append(order)

    def enroll_student(self, student: Student, group_number: str) -> None:
        group = self.faculty.get_group_strict(group_number)
        group.enroll_student(student)

        rb_number = f"ЗК-{student.record_book_number}-{group.number}"
        rb = RecordBook(student, rb_number)
        student.record_book = rb
        self.record_books[student] = rb
        self.record_books[student.person_id] = rb

    def get_student_record_book(self, student: Student | str) -> RecordBook:
        if isinstance(student, Student):
            if student.record_book is not None:
                return student.record_book
            if student in self.record_books:
                return self.record_books[student]
            key = student.person_id
        else:
            key = student

        if key not in self.record_books:
            raise StudentNotFoundException("Зачетная книжка для данного студента не заведена.")
        return self.record_books[key]

    def transfer_student(self, student: Student, from_group_num: str, to_group_num: str) -> None:
        from_group = self.faculty.get_group_strict(from_group_num)
        to_group = self.faculty.get_group_strict(to_group_num)
        order = TransferOrder(student, from_group, to_group)
        self._process_order(order)

    def expel_student_for_debts(
            self, student: Student, reason: str = "Академическая задолженность") -> None:
        order = ExpulsionOrder(student, reason)
        self._process_order(order)

    def issue_reprimand(self, student: Student, reason: str, is_strict: bool = False) -> None:
        order = ReprimandOrder(student, reason, is_strict)
        self._process_order(order)

    def summarize_session(self) -> None:
        excellent_students: list[Student] = []

        for group in self.faculty.groups:
            for student in group.students:
                if not student.is_active:
                    continue

                record_book = student.record_book or self.record_books.get(student) or self.record_books.get(student.person_id)
                if not record_book:
                    continue

                debts = record_book.get_debts()
                if len(debts) >= self.MAX_ALLOWED_DEBTS:
                    self.expel_student_for_debts(student)
                elif len(debts) == 0 and record_book.average_score >= self.MIN_SCHOLARSHIP_SCORE:
                    excellent_students.append(student)

        if excellent_students:
            schol_order = ScholarshipOrder(excellent_students)
            self._process_order(schol_order)

    @property
    def total_active_students(self) -> int:
        total = 0
        for group in self.faculty.groups:
            total += sum(1 for student in group.students if student.is_active)
        return total

    def get_all_debtors(self) -> list[Student]:
        debtors: list[Student] = []
        for group in self.faculty.groups:
            for student in group.students:
                if not student.is_active:
                    continue
                rb = student.record_book or self.record_books.get(student) or self.record_books.get(student.person_id)
                if rb and len(rb.get_debts()) > 0:
                    debtors.append(student)
        return debtors
