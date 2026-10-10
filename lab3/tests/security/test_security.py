import pytest
from datetime import UTC, datetime, timedelta
from lab3.domain.exceptions import SecurityCheckFailedException, VisaExpiredException
from lab3.domain.operations.baggage import Baggage
from lab3.domain.people.passenger import Passenger
from lab3.domain.people.security_officer import SecurityOfficer
from lab3.domain.security.customs_control import CustomsControl
from lab3.domain.security.customs_declaration import CustomsDeclaration
from lab3.domain.security.metal_detector import MetalDetector
from lab3.domain.security.passport_control import PassportControl
from lab3.domain.security.security_checkpoint import SecurityCheckpoint
from lab3.domain.security.visa import Visa
from lab3.domain.security.xray_scanner import XRayScanner


def test_security():
    p = Passenger("П", "П", "P-1")
    v_valid = Visa("USA", datetime.now(UTC) + timedelta(days=30))
    v_expired = Visa("USA", datetime.now(UTC) - timedelta(days=1))

    pc = PassportControl(1)
    pc.check_documents(p, v_valid, "USA")

    with pytest.raises(VisaExpiredException, match="Отсутствует виза"):
        pc.check_documents(p, None, "USA")

    with pytest.raises(VisaExpiredException, match="требуется виза China"):
        pc.check_documents(p, v_valid, "China")

    with pytest.raises(VisaExpiredException, match="истек"):
        pc.check_documents(p, v_expired, "USA")

    decl_ok = CustomsDeclaration(p, ["Вещи"], 5000.0)
    cc = CustomsControl()
    cc.inspect_declaration(decl_ok)
    assert decl_ok.is_approved is True

    decl_over = CustomsDeclaration(p, ["Деньги"], 15000.0)
    with pytest.raises(SecurityCheckFailedException):
        cc.inspect_declaration(decl_over)

    cp = SecurityCheckpoint(1)
    md = MetalDetector("MD-1")
    xr = XRayScanner("XR-1")
    officer = SecurityOfficer("О", "О", "P", 100.0)

    with pytest.raises(ValueError, match="не укомплектован"):
        cp.process_passenger(p)

    cp.assign_equipment(md, xr)
    with pytest.raises(ValueError, match="Нет дежурного офицера"):
        cp.process_passenger(p)

    officer.clock_in()
    cp.assign_officer(officer)
    bag = Baggage(10.0, p)
    cp.process_passenger(p, bag)
