from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from lab3.domain.exceptions import VisaExpiredException

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger
    from lab3.domain.security.visa import Visa


class PassportControl:
    def __init__(self, booth_number: int) -> None:
        self.booth_number = booth_number
        self._processed_count = 0

    @property
    def booth_id(self) -> str:
        return f"BOOTH-{self.booth_number}"

    @property
    def processed_count(self) -> int:
        return self._processed_count

    def check_documents(
        self, passenger: Passenger, visa: Visa | None, destination_country: str
    ) -> None:
        if not visa:
            raise VisaExpiredException(
                f"Отсутствует виза для въезда в страну {destination_country}."
            )
        if visa.country != destination_country:
            raise VisaExpiredException(
                f"В паспорте виза {visa.country}, требуется виза {destination_country}."
            )
        if not visa.is_valid(datetime.now(UTC)):
            raise VisaExpiredException("Срок действия визы истек.")
        self._processed_count += 1

    def stamp_entry(self, passenger: Passenger) -> str:
        return f"Штамп на въезд поставлен в паспорт {passenger.passport_number}"

    def deny_entry(self, passenger: Passenger, reason: str) -> str:
        return f"Въезд отклонен для пассажира {passenger.full_name} ({passenger.passport_number}): {reason}"

    def __repr__(self) -> str:
        return f"PassportControl(booth={self.booth_number}, processed={self._processed_count})"
