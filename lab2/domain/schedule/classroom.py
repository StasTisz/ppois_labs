from __future__ import annotations


class Classroom:
    def __init__(
        self,
        number: str,
        capacity: int,
        has_projector: bool = False,
        has_computers: bool = False,
    ) -> None:
        self.number = number
        self.capacity = capacity
        self.has_projector = has_projector
        self.has_computers = has_computers
        self._is_available = True

    @property
    def is_available(self) -> bool:
        return self._is_available

    def close_for_maintenance(self) -> None:
        self._is_available = False

    def open_classroom(self) -> None:
        self._is_available = True

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

    def __repr__(self) -> str:
        return f"Classroom(num={self.number!r}, cap={self.capacity}, computers={self.has_computers})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Classroom):
            return NotImplemented
        return self.number == other.number

    def __hash__(self) -> int:
        return hash(self.number)
