import pytest

from lab3.domain.people.passenger import Passenger
from lab3.domain.security.metal_detector import MetalDetector


def test_metal_detector():
    md = MetalDetector("Ceia-01", sensitivity_level=5)
    p = Passenger("П", "П", "P-MD")
    assert md.scan(p) is True
    assert md.test_alarm() is True

    md.set_sensitivity(8)
    assert md.sensitivity_level == 8

    with pytest.raises(ValueError):
        md.set_sensitivity(0)

    with pytest.raises(ValueError):
        md.set_sensitivity(11)

    md.is_active = False
    assert md.test_alarm() is False
    with pytest.raises(ValueError, match="выключен"):
        md.scan(p)
