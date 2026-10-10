from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from lab3.domain.exceptions import VisaExpiredException

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger
    from lab3.domain.security.visa import Visa


class PassportControl:
    def __init__(self, booth_number: int) -> None:
        self.booth_id = str(uuid.uuid4())
        self.booth_number = booth_number

    def check_documents(self, passenger: Passenger, visa: Visa | None, destination_country: str) -> None:
        if not visa:
            raise VisaExpiredException(f"Отсутствует виза для въезда в страну {destination_country}.")
        if visa.country != destination_country:
            raise VisaExpiredException(f"В паспорте виза {visa.country}, требуется виза {destination_country}.")
        if not visa.is_valid(datetime.now(UTC)):
            raise VisaExpiredException("Срок действия визы истек.")
