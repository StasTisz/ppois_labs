from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import BaggageOverweightException

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class Baggage:
    MAX_STANDARD_WEIGHT = 23.0

    def __init__(self, weight_kg: float, owner: Passenger | str) -> None:
        self.baggage_id = str(uuid.uuid4())
        self.weight_kg = weight_kg
        self.owner = owner if not isinstance(owner, str) else None
        self.owner_id = getattr(owner, "person_id", str(owner))

    def check_weight(self) -> None:
        if self.weight_kg > self.MAX_STANDARD_WEIGHT:
            raise BaggageOverweightException(
                f"Перевес: {self.weight_kg} кг. Максимум: {self.MAX_STANDARD_WEIGHT} кг."
            )
