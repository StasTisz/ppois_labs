import pytest
from lab2.domain.infrastructure.dormitory import Dormitory
from lab2.domain.infrastructure.room import Room
from lab2.domain.people.student import Student


def test_dormitory():
    dorm = Dormitory(1, "ул. Гикало 9")
    assert dorm.occupancy_rate == 0.0

    r1 = Room("101", capacity=2)
    dorm.add_room(r1)

    with pytest.raises(ValueError):
        dorm.add_room(Room("101", capacity=3))

    s1 = Student("С1", "С1")
    r1.check_in(s1)

    assert dorm.find_room_for_student(s1) == r1
    assert dorm.find_room_for_student(Student("С2", "С2")) is None
    assert len(dorm.get_available_rooms()) == 1
    assert dorm.occupancy_rate == 50.0
