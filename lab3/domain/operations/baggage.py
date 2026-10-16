"""Модуль зарегистрированного багажа пассажира."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import BaggageOverweightException

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class Baggage:
    """Единица багажа пассажира."""

    MAX_STANDARD_WEIGHT = 23.0
    _baggage_counter: int = 300000

    def __init__(
        self,
        weight_kg: float,
        owner: Passenger,
        tag_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса Baggage."""
        Baggage._baggage_counter += 1
        self.weight_kg = weight_kg
        self.owner = owner
        self.tag_number = tag_number or f"BAG-{Baggage._baggage_counter}"
        self._is_inspected = False

    @property
    def is_inspected(self) -> bool:
        """Возвращает признак inspected."""
        return self._is_inspected

    def check_weight(self) -> None:
        """Проверяет багаж на соответствие нормам провоза."""
        if self.weight_kg > self.MAX_STANDARD_WEIGHT:
            raise BaggageOverweightException(
                f"Перевес: {self.weight_kg} кг. Максимум: {self.MAX_STANDARD_WEIGHT} кг."
            )

    def attach_tag(self, tag: str) -> None:
        """Прикрепляет номерную багажную бирку к чемодану."""
        if not tag.strip():
            raise ValueError("Номер багажной бирки не может быть пустым.")
        self.tag_number = tag

    def inspect_contents(self) -> bool:
        """Проводит углубленный физический досмотр содержимого багажа."""
        self._is_inspected = True
        return True

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Baggage(tag={self.tag_number!r}, weight={self.weight_kg}kg, owner={self.owner.full_name!r})"
