import pytest
from lab2.domain.people.student import Student


def test_student():
    student = Student("Иван", "Иванов", "Иванович")
    assert student.is_active is True
    assert student.has_scholarship is False
    assert student.is_debtor is False

    student.financial_debt = 100.0
    assert student.is_debtor is True

    with pytest.raises(ValueError):
        student.pay_debt(-50)
    with pytest.raises(ValueError):
        student.pay_debt(0)

    student.pay_debt(40.0)
    assert student.financial_debt == 60.0
    student.pay_debt(1000.0)
    assert student.financial_debt == 0.0

    student.grant_scholarship()
    assert student.has_scholarship is True

    student.expel()
    assert student.is_active is False
    assert student.has_scholarship is False

    with pytest.raises(ValueError):
        student.grant_scholarship()
