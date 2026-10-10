import pytest
from lab3.domain.people.passenger import Passenger
from lab3.domain.security.metal_detector import MetalDetector


def test_metal_detector():
    md = MetalDetector("Ceia-01")
    p = Passenger("П", "П", "P-MD")
    assert md.scan(p) is True

    md.is_active = False
    with pytest.raises(ValueError):
        md.scan(p)
