from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.grading.grade import Grade

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.people.lecturer import Lecturer
    from lab2.domain.people.student import Student
    from lab2.domain.structure.academic_group import AcademicGroup


class AcademicStatement:
    def __init__(
        self,
        subject: Subject,
        group: AcademicGroup,
        examiner: Lecturer,
        statement_number: str = "",
    ) -> None:
        self.statement_number = (
            statement_number
            or f"STMT-{abs(hash((subject.name, group.number))) % 100000:05d}"
        )
        self.subject = subject
        self.group = group
        self.examiner = examiner
        self.is_closed = False
        self._results: dict[Student, Grade] = {}

    @property
    def results(self) -> dict[Student, Grade]:
        return self._results.copy()

    def add_result(self, student: Student, score: int) -> Grade:
        if self.is_closed:
            raise ValueError("Ведомость уже закрыта и передана в деканат.")
        grade = Grade(self.subject, score, is_exam=True, examiner=self.examiner)
        self._results[student] = grade
        return grade

    def get_student_grade(self, student: Student) -> Grade | None:
        return self._results.get(student)

    def close_statement(self) -> None:
        self.is_closed = True

    @property
    def pass_rate(self) -> float:
        if not self._results:
            return 0.0
        passed = sum(1 for grade in self._results.values() if grade.is_passed)
        return round((passed / len(self._results)) * 100.0, 2)

    def __repr__(self) -> str:
        return f"AcademicStatement(num={self.statement_number!r}, subject={self.subject.name!r}, group={self.group.number!r}, closed={self.is_closed})"
