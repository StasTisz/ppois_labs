import pytest
from lab2.domain.dean_office.dean_office import DeanOffice
from lab2.domain.exceptions import StudentNotFoundException
from lab2.domain.grading.grade import Grade
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.faculty import Faculty
from lab2.domain.structure.speciality import Speciality


def test_dean_office():
    dean = Dean("Декан", "Деканов")
    fitu = Faculty("ФИТиУ", "ФИТиУ")
    group1 = AcademicGroup("101", Speciality("1", "1"))
    group2 = AcademicGroup("102", Speciality("1", "1"))
    fitu.add_group(group1)
    fitu.add_group(group2)

    office = DeanOffice(fitu, dean)
    s1 = Student("Студент1", "А")
    s2 = Student("Студент2", "Б")

    office.enroll_student(s1, "101")
    office.enroll_student(s2, "101")
    assert office.total_active_students == 2

    rb = office.get_student_record_book(s1)
    assert rb == office.get_student_record_book(s1.person_id)

    with pytest.raises(StudentNotFoundException):
        office.get_student_record_book("fake-uuid")

    office.transfer_student(s1, "101", "102")
    assert s1 in group2.students
    assert s1 not in group1.students

    office.issue_reprimand(s1, "Замечание", is_strict=False)

    rb.add_grade(Grade("Математика", 2, is_exam=True))
    assert s1 in office.get_all_debtors()

    rb.add_grade(Grade("Физика", 2, is_exam=True))
    rb.add_grade(Grade("Химия", 2, is_exam=True))
    office.summarize_session()
    assert s1.is_active is False

    rb2 = office.get_student_record_book(s2)
    rb2.add_grade(Grade("ООП", 10, is_exam=True))
    office.summarize_session()
    assert s2.has_scholarship is True
