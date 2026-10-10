import pytest
from lab3.domain.operations.baggage import Baggage
from lab3.domain.people.passenger import Passenger
from lab3.domain.people.security_officer import SecurityOfficer
from lab3.domain.security.metal_detector import MetalDetector
from lab3.domain.security.security_checkpoint import SecurityCheckpoint
from lab3.domain.security.xray_scanner import XRayScanner


def test_security_checkpoint():
    cp = SecurityCheckpoint(1)
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
    cp.process_passenger(p, bag)
