import pytest

from lab3.domain.exceptions import SecurityCheckFailedException
from lab3.domain.people.passenger import Passenger
from lab3.domain.security.customs_control import CustomsControl
from lab3.domain.security.customs_declaration import CustomsDeclaration


def test_customs_control():
    cc = CustomsControl(control_number=2)
    assert cc.control_id == "CC-2"
    assert cc.inspections_count == 0
    assert "CustomsControl" in repr(cc)

    p = Passenger("П", "П", "P-CC")

    decl_ok = CustomsDeclaration(p, ["Личные вещи"], 4000.0)
    cc.inspect_declaration(decl_ok)
    assert decl_ok.is_approved is True
    assert cc.inspections_count == 1

    decl_fail = CustomsDeclaration(p, ["Валюта"], 12000.0)
    with pytest.raises(SecurityCheckFailedException):
        cc.inspect_declaration(decl_fail)

    excess = cc.confiscate_excess(decl_fail)
    assert excess == 2000.0
    assert decl_fail.cash_amount == 10000.0
    assert cc.confiscate_excess(decl_ok) == 0.0

    stamp_msg = cc.stamp_passport(p)
    assert "P-CC" in stamp_msg
