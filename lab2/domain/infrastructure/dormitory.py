from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.infrastructure.room import Room

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class Dormitory:
    def __init__(self, number: int, address: str) -> None:
        self.number = number
        self.address = address
        self._rooms: list[Room] = []

    def add_room(self, room: Room) -> None:
        if any(r.number == room.number for r in self._rooms):
            raise ValueError(f"Комната {room.number} уже есть в плане общежития.")
        self._rooms.append(room)

    def find_room_for_student(self, student: Student) -> Room | None:
        if getattr(student, "room", None) and student.room in self._rooms:
            return student.room
        for room in self._rooms:
            if room.has_resident(student):
                return room
        return None

    def get_available_rooms(self) -> list[Room]:
        return [room for room in self._rooms if room.free_beds > 0]

    @property
    def occupancy_rate(self) -> float:
        if not self._rooms:
            return 0.0
        total_beds = sum(r.capacity for r in self._rooms)
        taken_beds = sum(r.capacity - r.free_beds for r in self._rooms)
        return round((taken_beds / total_beds) * 100, 2)
