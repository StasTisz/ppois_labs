from lab3.domain.people.passenger import Passenger
from lab3.domain.security.customs_declaration import CustomsDeclaration


def test_customs_declaration():
    p = Passenger("П", "П", "P-CD")
    decl = CustomsDeclaration(p, ["Камера", "Ноутбук"], cash_amount=3000.0)
    assert decl.passenger == p
    assert decl.is_approved is False

    decl.approve()
    assert decl.is_approved is True
