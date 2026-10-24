from datetime import UTC, datetime, timedelta

import pytest

from lab3.domain.exceptions import VisaExpiredException
from lab3.domain.people.passenger import Passenger
from lab3.domain.security.passport_control import PassportControl
from lab3.domain.security.visa import Visa


def test_passport_control():
    pc = PassportControl(4)
    assert pc.booth_id == "BOOTH-4"
    assert pc.processed_count == 0
    assert "PassportControl" in repr(pc)

    p = Passenger("П", "П", "P-PC")
    now = datetime.now(UTC)
    visa_ok = Visa("Turkey", now + timedelta(days=15))
    visa_exp = Visa("Turkey", now - timedelta(days=1))

    pc.check_documents(p, visa_ok, "Turkey")
    assert pc.processed_count == 1

    stamp_msg = pc.stamp_entry(p)
    assert "P-PC" in stamp_msg

    deny_msg = pc.deny_entry(p, "Нарушение порядка")
    assert "Нарушение порядка" in deny_msg

    with pytest.raises(VisaExpiredException, match="Отсутствует виза"):
        pc.check_documents(p, None, "Turkey")

    with pytest.raises(VisaExpiredException, match="требуется виза Japan"):
        pc.check_documents(p, visa_ok, "Japan")

    with pytest.raises(VisaExpiredException, match="истек"):
        pc.check_documents(p, visa_exp, "Turkey")
