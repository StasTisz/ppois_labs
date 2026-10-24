import pytest

from lab2.domain.documents.scholarship_order import ScholarshipOrder
from lab2.domain.exceptions import DocumentNotSignedException
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student


def test_scholarship_order():
    s1 = Student("С1", "С1")
    s2 = Student("С2", "С2")
    dean = Dean("Д", "Д")

    order = ScholarshipOrder([s1])
    assert len(order.students) == 1
    order.add_student(s2)
    assert len(order.students) == 2

    s3 = Student("С3", "С3")
    s3.expel()
    with pytest.raises(ValueError, match="неактивному"):
        order.add_student(s3)

    order.remove_student(s2)
    assert len(order.students) == 1

    with pytest.raises(DocumentNotSignedException):
        order.execute()

    order.sign(dean)
    order.execute()
    assert s1.has_scholarship is True
