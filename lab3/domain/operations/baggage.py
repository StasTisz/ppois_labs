from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import BaggageOverweightException

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class Baggage:
    MAX_STANDARD_WEIGHT = 23.0

    def __init__(
        self,
        weight_kg: float,
        owner: Passenger | str,
        tag_number: str = "",
    ) -> None:
        self.weight_kg = weight_kg
        self.weight = weight_kg
        if isinstance(owner, str):
            self.owner: Passenger | None = None
            self._owner_id_fallback: str | None = owner
        else:
            self.owner = owner
            self._owner_id_fallback = None

        owner_ident = getattr(owner, "passport_number", str(owner))
        self.tag_number = (
            tag_number or f"BAG-{abs(hash((owner_ident, weight_kg))) % 1000000:06d}"
        )
        self._is_inspected = False

    @property
    def owner_id(self) -> str:
        if self.owner is not None:
            return getattr(self.owner, "person_id", self.owner.passport_number)
        return self._owner_id_fallback or ""

    @property
    def is_inspected(self) -> bool:
        return self._is_inspected

    def check_weight(self) -> None:
        if self.weight_kg > self.MAX_STANDARD_WEIGHT:
            raise BaggageOverweightException(
                f"Перевес: {self.weight_kg} кг. Максимум: {self.MAX_STANDARD_WEIGHT} кг."
            )

    def attach_tag(self, tag: str) -> None:
        if not tag.strip():
            raise ValueError("Номер багажной бирки не может быть пустым.")
        self.tag_number = tag

    def inspect_contents(self) -> bool:
        self._is_inspected = True
        return True

    def __repr__(self) -> str:
        owner_name = self.owner.full_name if self.owner else self._owner_id_fallback
        return f"Baggage(tag={self.tag_number!r}, weight={self.weight_kg}kg, owner={owner_name!r})"
