import pytest

from lab3.domain.security.scanner import Scanner


class DummyScanner(Scanner):
    def scan(self, target) -> bool:
        return self.is_active


def test_scanner():
    s = DummyScanner("Scan-100", serial_number="SCN-999")
    assert s.model == "Scan-100"
    assert s.scanner_id == "SCN-999"
    assert s.is_calibrated is True
    assert s.scan(None) is True
    assert "DummyScanner" in repr(s)

    assert s.calibrate() is True

    s.toggle_power()
    assert s.is_active is False
    with pytest.raises(ValueError, match="выключенный сканер"):
        s.calibrate()
