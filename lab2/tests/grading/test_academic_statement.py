import pytest
from lab2.domain.academics.subject import Subject
from lab2.domain.grading.academic_statement import AcademicStatement
from lab2.domain.people.lecturer import Lecturer
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_academic_statement():
    subj = Subject("ООП", 1)
    group = AcademicGroup("1", Speciality("1", "1"))
    lect = Lecturer("Л", "Л")
    stmt = AcademicStatement(subj, group, lect)

    assert stmt.pass_rate == 0.0
    assert stmt.is_closed is False

    s1 = Student("A", "A")
    s2 = Student("B", "B")

    stmt.add_result(s1, 10)
    stmt.add_result(s2, 2)
    assert stmt.pass_rate == 50.0

    stmt.close_statement()
    assert stmt.is_closed is True
    with pytest.raises(ValueError):
        stmt.add_result(s1, 5)
