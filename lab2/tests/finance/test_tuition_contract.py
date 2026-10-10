import pytest
from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.finance.tuition_contract import TuitionContract
from lab2.domain.people.student import Student


def test_tuition_contract():
    s = Student("S", "S")
    acc = BankAccount(s, "ACC1")
    acc.deposit(1000)
    c = TuitionContract("C-1", s, 1000.0)

    assert c.debt == 1000.0
    assert c.is_fully_paid is False
    assert c.is_signed is False

    with pytest.raises(ValueError):
        c.pay_tuition(100, acc)

    c.sign_contract()
    assert c.is_signed is True
    assert s.financial_debt == 1000.0

    c.pay_tuition(100, acc)
    assert c.paid_amount == 100.0
    assert c.debt == 900.0
    assert s.financial_debt == 900.0
    assert c.is_overdue is True

    c.apply_discount(10)
    assert c.total_amount == 900.0
    assert c.debt == 800.0

    with pytest.raises(ValueError):
        c.apply_discount(-5)
    with pytest.raises(ValueError):
        c.apply_discount(105)

    c.pay_tuition(800, acc)
    assert c.is_fully_paid is True
    assert c.is_overdue is False
