import pytest

from lab3.domain.exceptions import SecurityCheckFailedException
from lab3.domain.operations.baggage import Baggage
from lab3.domain.people.passenger import Passenger
from lab3.domain.people.security_officer import SecurityOfficer
from lab3.domain.security.metal_detector import MetalDetector
from lab3.domain.security.security_checkpoint import SecurityCheckpoint
from lab3.domain.security.xray_scanner import XRayScanner


class FailingMetalDetector(MetalDetector):
    def scan(self, target) -> bool:
        return False


def test_security_checkpoint():
    cp = SecurityCheckpoint(1)
    assert cp.checkpoint_id == "CP-1"
    assert cp.processed_passengers_count == 0
    assert cp.is_ready_for_service() is False
    assert "SecurityCheckpoint" in repr(cp)

    p = Passenger("П", "П", "P-CP")
    bag = Baggage(8.0, p)
    officer = SecurityOfficer("О", "О", "P-SO", 1200.0)

    with pytest.raises(ValueError, match="не укомплектован"):
        cp.process_passenger(p)

    cp.assign_equipment(MetalDetector("MD"), XRayScanner("XR"))
    with pytest.raises(ValueError, match="Нет дежурного офицера"):
        cp.process_passenger(p)

    officer.clock_in()
    cp.assign_officer(officer)
    assert cp.is_ready_for_service() is True

    cp.process_passenger(p, bag)
    assert cp.processed_passengers_count == 1

    cp.close_checkpoint()
    assert cp.is_open is False
    with pytest.raises(ValueError, match="закрыт"):
        cp.process_passenger(p)

    cp.open_checkpoint()
    # Test SecurityCheckFailedException
    cp.assign_equipment(FailingMetalDetector("Failing"), XRayScanner("XR"))
    with pytest.raises(SecurityCheckFailedException):
        cp.process_passenger(p)
