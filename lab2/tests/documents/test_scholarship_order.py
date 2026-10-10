import pytest
from lab2.domain.documents.scholarship_order import ScholarshipOrder
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student


def test_scholarship_order():
    s1 = Student("С1", "С1")
    s2 = Student("С2", "С2")
    dean = Dean("Д", "Д")

    order = ScholarshipOrder([s1, s2])
    with pytest.raises(ValueError):
        order.execute()

    order.sign(dean)
    order.execute()
    assert s1.has_scholarship is True
    assert s2.has_scholarship is True
