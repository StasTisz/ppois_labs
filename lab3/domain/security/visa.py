from __future__ import annotations

import uuid
from datetime import datetime, timedelta


class Visa:
    def __init__(
        self,
        country: str,
        expiration_date: datetime,
        visa_number: str | None = None,
    ) -> None:
        self.visa_number = visa_number or f"V-{str(uuid.uuid4())[:8].upper()}"
        self.country = country
        self.expiration_date = expiration_date
        self._is_revoked = False

    @property
    def visa_id(self) -> str:
        return self.visa_number

    @property
    def is_revoked(self) -> bool:
        return self._is_revoked

    def is_valid(self, current_date: datetime) -> bool:
        if self._is_revoked:
            return False
        return current_date <= self.expiration_date

    def extend_validity(self, days: int) -> None:
        if self._is_revoked:
            raise ValueError(f"Нельзя продлить отозванную визу {self.visa_number}.")
        if days <= 0:
            raise ValueError("Количество дней продления должно быть положительным.")
        self.expiration_date += timedelta(days=days)

    def revoke(self) -> None:
        self._is_revoked = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Visa):
            return False
        return self.visa_number == other.visa_number

    def __repr__(self) -> str:
        return f"Visa(number={self.visa_number!r}, country={self.country!r}, valid_until={self.expiration_date.isoformat()})"
