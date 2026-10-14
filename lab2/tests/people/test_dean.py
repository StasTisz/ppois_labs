import pytest

from lab2.domain.documents.expulsion_order import ExpulsionOrder
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student


def test_dean():
    dean = Dean("Декан", "Деканов")
    s = Student("Студент", "Студентов")
    order = ExpulsionOrder(s, "Пропуски занятий длительное время")
    result = dean.sign_order(order)
    assert "ПРИКАЗ УТВЕРЖДЕН: Приказ об отчислении" in result
    assert "Деканов Декан" in result
    assert dean.signed_orders_count == 1
    assert order.is_signed is True

    inst = dean.issue_instruction("Провести старостат в среду")
    assert "Провести старостат" in inst

    with pytest.raises(ValueError):
        dean.issue_instruction("   ")

    dean.veto_order(order, "Недостаточно оснований")
    assert order.cancellation_reason is not None

    with pytest.raises(ValueError):
        dean.veto_order(order, "")
