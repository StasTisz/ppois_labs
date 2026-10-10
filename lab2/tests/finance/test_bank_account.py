import pytest
from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.people.student import Student


def test_bank_account():
    s = Student("С", "С")
    acc1 = BankAccount(s, "A1")
    assert acc1.owner == s
    assert acc1.owner_id == s.person_id
    assert s.bank_account == acc1

    acc2 = BankAccount("user2", "A2")
    assert acc2.owner_id == "user2"

    with pytest.raises(ValueError):
        acc1.deposit(-10)
    with pytest.raises(ValueError):
        acc1.deposit(0)

    acc1.deposit(100)
    assert acc1.balance == 100.0

    with pytest.raises(ValueError):
        acc1.withdraw(-10)
    with pytest.raises(ValueError):
        acc1.withdraw(0)
    with pytest.raises(ValueError):
        acc1.withdraw(1000)

    acc1.withdraw(40)
    assert acc1.balance == 60.0

    acc1.transfer_to(acc2, 20)
    assert acc1.balance == 40.0
    assert acc2.balance == 20.0

    with pytest.raises(ValueError):
        acc1.transfer_to(acc1, 10)

    acc1.block_account()
    assert acc1.is_blocked is True
    with pytest.raises(ValueError):
        acc1.withdraw(10)
