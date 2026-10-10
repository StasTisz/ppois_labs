import pytest
from lab2.domain.documents.transfer_order import TransferOrder
from lab2.domain.exceptions import DocumentNotSignedException
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_transfer_order():
    s = Student("С", "С")
    dean = Dean("Д", "Д")
    spec = Speciality("1", "1")
    g1 = AcademicGroup("1", spec)
    g2 = AcademicGroup("2", spec)
    g1.enroll_student(s)

    order = TransferOrder(s, g1, g2)
    with pytest.raises(DocumentNotSignedException):
        order.execute()

    order.sign(dean)
    order.execute()
    assert s not in g1.students
    assert s in g2.students
