"""Модуль въездной визы пассажира."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta


class Visa:
    """Виза для пересечения границы."""

    def __init__(
        self,
        country: str,
        expiration_date: datetime,
        visa_number: str | None = None,
    ) -> None:
        """Инициализирует экземпляр класса Visa."""
        self.visa_number = visa_number or f"V-{str(uuid.uuid4())[:8].upper()}"
        self.country = country
        self.expiration_date = expiration_date
        self._is_revoked = False

    @property
    def visa_id(self) -> str:
        """Возвращает значение атрибута visa_id."""
        return self.visa_number

    @property
    def is_revoked(self) -> bool:
        """Возвращает признак revoked."""
        return self._is_revoked

    def is_valid(self, current_date: datetime) -> bool:
        """Проверяет, не истек ли срок действия визы на указанную дату."""
        if self._is_revoked:
            return False
        return current_date <= self.expiration_date

    def extend_validity(self, days: int) -> None:
        """Продлевает срок действия въездной визы на указанное число дней."""
        if self._is_revoked:
            raise ValueError(f"Нельзя продлить отозванную визу {self.visa_number}.")
        if days <= 0:
            raise ValueError("Количество дней продления должно быть положительным.")
        self.expiration_date += timedelta(days=days)

    def revoke(self) -> None:
        """Аннулирует въездную визу пассажира."""
        self._is_revoked = True

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Visa):
            return False
        return self.visa_number == other.visa_number

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Visa(number={self.visa_number!r}, country={self.country!r}, valid_until={self.expiration_date.isoformat()})"
