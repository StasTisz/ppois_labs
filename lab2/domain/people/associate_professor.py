from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.grading.grade import Grade
from lab2.domain.people.lecturer import Lecturer

if TYPE_CHECKING:
    from lab2.domain.academics.subject import Subject
    from lab2.domain.people.student import Student
    from lab2.domain.structure.academic_group import AcademicGroup


class AssociateProfessor(Lecturer):
    DEFAULT_DEGREE = "К.т.н."
    DEFAULT_POSITION = "Доцент"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = DEFAULT_DEGREE,
        passport_number: str = "",
        published_papers_count: int = 5,
        research_field: str = "Информационные технологии",
    ) -> None:
        super().__init__(
            first_name,
            last_name,
            middle_name,
            degree=degree,
            position=self.DEFAULT_POSITION,
            passport_number=passport_number,
        )
        self.published_papers_count = published_papers_count
        self.research_field = research_field

    def publish_paper(self, title: str) -> str:
        self.published_papers_count += 1
        return f"Опубликована научная статья '{title}' в области '{self.research_field}'."

    def conduct_lecture(self, subject: Subject, group: AcademicGroup) -> str:
        return (
            f"Доцент {self.full_name} прочитал лекцию по предмету '{subject.name}' "
            f"для потока группы {group.number}."
        )

    def review_coursework(
        self, student: Student, subject: Subject, score: int
    ) -> Grade:
        grade = Grade(subject, score, is_exam=False, examiner=self)
        return grade

    def publish_methodology(self, title: str, pages: int) -> str:
        if pages <= 0:
            raise ValueError("Объем методички должен быть положительным.")
        return f"Методическое пособие '{title}' ({pages} стр.) рекомендовано к изданию доцентом {self.full_name}."
