import pytest
from lab2.domain.documents.reprimand_order import ReprimandOrder
from lab2.domain.exceptions import DocumentNotSignedException
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student


def test_reprimand_order():
    s = Student("С", "С")
    s.has_scholarship = True
    dean = Dean("Д", "Д")

    rep1 = ReprimandOrder(s, "Опоздание", is_strict=False)
    with pytest.raises(DocumentNotSignedException):
        rep1.execute()

    rep1.sign(dean)
    rep1.execute()
    assert s.has_scholarship is True

    rep2 = ReprimandOrder(s, "Прогулы", is_strict=True)
    rep2.sign(dean)
    rep2.execute()
    assert s.has_scholarship is False
