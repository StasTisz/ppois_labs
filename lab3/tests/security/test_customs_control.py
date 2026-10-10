import pytest
from lab3.domain.exceptions import SecurityCheckFailedException
from lab3.domain.people.passenger import Passenger
from lab3.domain.security.customs_control import CustomsControl
from lab3.domain.security.customs_declaration import CustomsDeclaration


def test_customs_control():
    cc = CustomsControl()
    p = Passenger("П", "П", "P-CC")

    decl_ok = CustomsDeclaration(p, ["Личные вещи"], 4000.0)
    cc.inspect_declaration(decl_ok)
    assert decl_ok.is_approved is True

    decl_fail = CustomsDeclaration(p, ["Валюта"], 12000.0)
    with pytest.raises(SecurityCheckFailedException):
        cc.inspect_declaration(decl_fail)
