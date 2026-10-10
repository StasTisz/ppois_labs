from __future__ import annotations

import uuid


class Classroom:
    def __init__(
            self, number: str, capacity: int, has_projector: bool = False, has_computers: bool = False
    ) -> None:
        self.room_id = str(uuid.uuid4())
        self.number = number
        self.capacity = capacity
        self.has_projector = has_projector
        self.has_computers = has_computers
        self.is_available = True

    def close_for_maintenance(self) -> None:
        self.is_available = False

    def open_classroom(self) -> None:
        self.is_available = True

    def equip_with_computers(self, update_capacity_by: int = 0) -> None:
        new_capacity = self.capacity + update_capacity_by
        if new_capacity <= 0:
            raise ValueError(
                f"Недопустимая вместимость: {new_capacity}. "
                f"Аудитория должна вмещать хотя бы одного человека."
            )
        self.has_computers = True
        self.capacity = new_capacity

    def remove_projector(self) -> None:
        self.has_projector = False
