import pytest
from lab2.domain.exceptions import DuplicateEnrollmentException
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_academic_group():
    spec = Speciality("ИИ", "Искусственный интеллект")
    group = AcademicGroup("101", spec, max_students=2)
    assert "Группа 101" in str(group)
    assert group.students_count == 0
    assert group.has_vacancies is True
    assert group.is_full() is False

    s1 = Student("А", "Б")
    s2 = Student("В", "Г")
    s3 = Student("Д", "Е")

    group.enroll_student(s1)
    assert s1.group == group
    assert s1 in group.students
    assert len(group.active_students) == 1

    with pytest.raises(DuplicateEnrollmentException):
        group.enroll_student(s1)

    group.enroll_student(s2)
    assert group.is_full() is True
    with pytest.raises(ValueError, match="переполнена"):
        group.enroll_student(s3)

    group.expel_student(s1)
    assert s1 not in group.students
    assert s1.group is None
    assert group.has_vacancies is True

    s2.expel()
    assert len(group.active_students) == 0
    group.clear_expelled()
    assert group.students_count == 0
