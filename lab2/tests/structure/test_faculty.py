import pytest
from lab2.domain.exceptions import GroupNotFoundException
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.department import Department
from lab2.domain.structure.faculty import Faculty
from lab2.domain.structure.speciality import Speciality


def test_faculty():
    f = Faculty("ФИТиУ", "ФИТиУ")
    spec = Speciality("1", "1")
    g = AcademicGroup("101", spec)
    s = Student("Студент", "Студентов")
    g.enroll_student(s)

    dept = Department("Кафедра ИТ")
    f.add_department(dept)

    f.add_group(g)
    with pytest.raises(ValueError):
        f.add_group(g)

    assert f.find_group("101") == g
    assert f.find_group("999") is None
    assert f.get_group_strict("101") == g

    with pytest.raises(GroupNotFoundException):
        f.get_group_strict("999")

    assert f.find_student_by_id(s.person_id) == s
    assert f.find_student_by_id("fake-id") is None
    assert f.get_total_capacity() == 30
    assert len(f.groups) == 1
