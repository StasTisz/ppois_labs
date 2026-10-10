import pytest
from lab2.domain.documents.academic_leave_order import AcademicLeaveOrder
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student


def test_academic_leave_order():
    s = Student("С", "С")
    s.has_scholarship = True
    dean = Dean("Д", "Д")

    order = AcademicLeaveOrder(s, "Болезнь", 12)
    assert order.duration_months == 12

    with pytest.raises(ValueError):
        order.execute()

    order.sign(dean)
    order.execute()
    assert s.is_active is False
    assert s.has_scholarship is False
