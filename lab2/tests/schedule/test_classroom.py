import pytest
from lab2.domain.schedule.classroom import Classroom


def test_classroom():
    room = Classroom("101", 30, has_computers=False)
    assert room.is_available is True
    room.close_for_maintenance()
    assert room.is_available is False
    room.open_classroom()
    assert room.is_available is True

    room.remove_projector()
    assert room.has_projector is False

    room.equip_with_computers(5)
    assert room.has_computers is True
    assert room.capacity == 35

    with pytest.raises(ValueError):
        room.equip_with_computers(-35)
