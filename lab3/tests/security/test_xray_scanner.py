import pytest
from lab3.domain.operations.baggage import Baggage
from lab3.domain.people.passenger import Passenger
from lab3.domain.security.xray_scanner import XRayScanner


def test_xray_scanner():
    xr = XRayScanner("Smiths-01")
    bag = Baggage(10.0, Passenger("П", "П", "P-XR"))
    assert xr.scan(bag) is True

    xr.is_active = False
    with pytest.raises(ValueError):
        xr.scan(bag)
