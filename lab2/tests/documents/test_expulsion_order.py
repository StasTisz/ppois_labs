import pytest
from lab2.domain.documents.expulsion_order import ExpulsionOrder
from lab2.domain.exceptions import DocumentNotSignedException, ExpulsionDeniedException
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student


def test_expulsion_order():
    s = Student("С", "С")
    dean = Dean("Д", "Д")
    order = ExpulsionOrder(s, "Академическая задолженность")

    with pytest.raises(DocumentNotSignedException):
        order.execute()

    order.sign(dean)
    order.execute()
    assert s.is_active is False

    s2 = Student("С2", "С2")
    order_invalid = ExpulsionOrder(s2, "Просто так")
    order_invalid.sign(dean)
    with pytest.raises(ExpulsionDeniedException):
        order_invalid.execute()

    s3 = Student("С3", "С3")
    order_vol = ExpulsionOrder(s3, "По собственному желанию")
    order_vol.sign(dean)
    order_vol.execute()
    assert s3.is_active is False
