from datetime import UTC, datetime, timedelta
from lab3.domain.security.visa import Visa


def test_visa():
    now = datetime.now(UTC)
    visa = Visa("Schengen", now + timedelta(days=60))
    assert visa.is_valid(now) is True
    assert visa.is_valid(now + timedelta(days=90)) is False
