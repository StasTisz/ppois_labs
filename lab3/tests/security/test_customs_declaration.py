import pytest

from lab3.domain.people.passenger import Passenger
from lab3.domain.security.customs_declaration import CustomsDeclaration


def test_customs_declaration():
    p = Passenger("П", "П", "P-CD")
    decl = CustomsDeclaration(
        p, ["Камера", "Ноутбук"], cash_amount=3000.0, declaration_number="DEC-01"
    )
    assert decl.passenger == p
    assert decl.passenger_id == "P-CD"
    assert decl.declaration_id == "DEC-01"
    assert decl.is_approved is False
    assert len(decl.declared_items) == 2
    assert decl.cash_amount == 3000.0
    assert "CustomsDeclaration" in repr(decl)

    # Test copy protection
    items = decl.declared_items
    items.append("Часы")
    assert "Часы" not in decl.declared_items

    decl.add_item("Часы")
    assert len(decl.declared_items) == 3

    decl.declare_cash(4500.0)
    assert decl.cash_amount == 4500.0

    with pytest.raises(ValueError):
        decl.declare_cash(-100.0)

    decl.approve()
    assert decl.is_approved is True

    with pytest.raises(ValueError, match="одобренную"):
        decl.add_item("Золото")

    with pytest.raises(ValueError, match="одобренную"):
        decl.declare_cash(5000.0)

    decl.reject()
    assert decl.is_approved is False
