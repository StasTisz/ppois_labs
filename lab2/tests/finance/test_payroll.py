import pytest
from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.finance.payroll import Payroll
from lab2.domain.people.employee import Employee
from lab2.domain.people.student import Student


def test_payroll():
    pay = Payroll(10, 2026)
    acc = BankAccount("test", "1")
    emp = Employee("E", "E")
    emp.salary = 500.0

    pay.pay_salary(emp, acc, bonus=50.0)
    assert acc.balance == 550.0
    assert pay.total_fund == 550.0

    s = Student("S", "S")
    s.has_scholarship = False
    with pytest.raises(ValueError):
        pay.pay_scholarship(s, acc)

    s.has_scholarship = True
    pay.pay_scholarship(s, acc)
    assert acc.balance == 670.0
    assert pay.total_fund == 670.0
    assert pay.total_payments_count == 2
    assert len(pay.get_payment_history()) == 2
