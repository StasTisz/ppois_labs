import pytest

from lab2.domain.academics.subject import Subject
from lab2.domain.people.associate_professor import AssociateProfessor
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_associate_professor():
    ap = AssociateProfessor("Доцент", "Доцентов")
    assert ap.degree == "К.т.н."

    subj = Subject("Базы Данных", 2)
    group = AcademicGroup("201", Speciality("ИСиТ", "ISIT-01"))
    student = Student("Петр", "Петров")

    msg = ap.conduct_lecture(subj, group)
    assert "прочитал лекцию" in msg

    grade = ap.review_coursework(student, subj, 9)
    assert grade.score == 9
    assert grade.examiner == ap

    pub = ap.publish_methodology("Методические указания к ЛР", 45)
    assert "рекомендовано к изданию" in pub

    with pytest.raises(ValueError):
        ap.publish_methodology("Ошибочная", 0)
