from datetime import UTC, datetime, timedelta

import pytest

from lab3.domain.security.visa import Visa


def test_visa():
    now = datetime.now(UTC)
    visa = Visa("Schengen", now + timedelta(days=60), visa_number="V-123456")
    assert visa.is_valid(now) is True
    assert visa.is_valid(now + timedelta(days=90)) is False
    assert visa.visa_id == "V-123456"
    assert "Visa" in repr(visa)
    assert visa == Visa("Schengen", now, visa_number="V-123456")
    assert visa != "NotAVisa"

    visa.extend_validity(30)
    assert visa.is_valid(now + timedelta(days=70)) is True

    with pytest.raises(ValueError):
        visa.extend_validity(-5)

    visa.revoke()
    assert visa.is_revoked is True
    assert visa.is_valid(now) is False

    with pytest.raises(ValueError, match="отозванную"):
        visa.extend_validity(10)
