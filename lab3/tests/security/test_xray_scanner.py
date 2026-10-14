import pytest

from lab3.domain.operations.baggage import Baggage
from lab3.domain.people.passenger import Passenger
from lab3.domain.security.xray_scanner import XRayScanner


def test_xray_scanner():
    xr = XRayScanner("Smiths-01", contrast_level=1.0)
    bag = Baggage(10.0, Passenger("П", "П", "P-XR"))
    assert xr.scan(bag) is True
    assert xr.detect_organic_materials(bag) is True

    xr.adjust_contrast(1.5)
    assert xr.contrast_level == 1.5

    with pytest.raises(ValueError):
        xr.adjust_contrast(-0.5)

    xr.is_active = False
    with pytest.raises(ValueError):
        xr.scan(bag)

    with pytest.raises(ValueError):
        xr.detect_organic_materials(bag)
