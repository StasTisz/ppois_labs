from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.infrastructure.room import Room

if TYPE_CHECKING:
    from lab2.domain.people.student import Student


class Dormitory:
    DEFAULT_COMMANDANT = "Иванова А.В."

    def __init__(
        self,
        number: int,
        address: str,
        commandant_name: str = DEFAULT_COMMANDANT,
    ) -> None:
        self.number = number
        self.address = address
        self.commandant_name = commandant_name
        self._rooms: list[Room] = []

    @property
    def rooms(self) -> list[Room]:
        return list(self._rooms)

    def add_room(self, room: Room) -> None:
        if any(room_item.number == room.number for room_item in self._rooms):
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

    def evict_student(self, student: Student) -> bool:
        room = self.find_room_for_student(student)
        if room:
            room.evict(student)
            return True
        return False

    @property
    def total_residents_count(self) -> int:
        return sum(len(room.residents) for room in self._rooms)

    @property
    def occupancy_rate(self) -> float:
        if not self._rooms:
            return 0.0
        total_beds = sum(room_item.capacity for room_item in self._rooms)
        taken_beds = sum(
            room_item.capacity - room_item.free_beds for room_item in self._rooms
        )
        return round((taken_beds / total_beds) * 100.0, 2)

    def __repr__(self) -> str:
        return f"Dormitory(num={self.number}, address={self.address!r}, rooms_count={len(self._rooms)})"
