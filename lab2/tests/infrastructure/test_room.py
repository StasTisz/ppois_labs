import pytest
from lab2.domain.exceptions import ResidentNotFoundException, RoomCapacityExceededException
from lab2.domain.infrastructure.room import Room
from lab2.domain.people.student import Student


def test_room():
    room = Room("101", capacity=1)
    assert room.capacity == 1
    assert room.free_beds == 1
    assert room.is_empty is True

    s1 = Student("А", "Б")
    room.check_in(s1)
    assert s1.room == room
    assert room.has_resident(s1) is True
    assert room.free_beds == 0
    assert room.is_empty is False

    with pytest.raises(ValueError):
        room.check_in(s1)

    s2 = Student("В", "Г")
    with pytest.raises(RoomCapacityExceededException):
        room.check_in(s2)

    with pytest.raises(ResidentNotFoundException):
        room.evict(s2)

    room.evict(s1)
    assert s1.room is None
    assert room.is_empty is True

    room.check_in(s1)
    room.evict_all()
    assert room.is_empty is True
    assert s1.room is None
