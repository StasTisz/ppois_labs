"""Модуль грузчика службы обработки багажа."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight import Flight


class BaggageHandler(Employee):
    """Грузчик багажного отделения."""

    HEAVY_MACHINERY_LOAD_TONS: float = 2.0
    MANUAL_LOAD_TONS: float = 0.5
    KG_PER_TON: float = 1000.0

    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        heavy_machinery_license: bool = True,
    ) -> None:
        """Инициализирует экземпляр класса BaggageHandler."""
        super().__init__(first_name, last_name, passport_number, salary)
        self.heavy_machinery_license = heavy_machinery_license
        self._tons_loaded = 0.0

    @property
    def tons_loaded(self) -> float:
        """Общий тоннаж погруженного багажа за смену."""
        return self._tons_loaded

    def perform_duty(self) -> str:
        """Осуществляет погрузку чемоданов в трюм или на тележку."""
        if self.heavy_machinery_license:
            self._tons_loaded += self.HEAVY_MACHINERY_LOAD_TONS
            return f"Грузчик {self.full_name} загружает багаж с помощью погрузчика."
        self._tons_loaded += self.MANUAL_LOAD_TONS
        return f"Грузчик {self.full_name} загружает багаж вручную."

    def load_to_cargo_hold(self, flight: Flight, baggage: Baggage) -> None:
        """Загружает проверенный багаж в грузовой отсек самолета."""
        if not self.is_on_shift:
            raise ValueError(f"Грузчик {self.full_name} не на смене.")
        if flight.status == "Cancelled":
            raise ValueError(f"Рейс {flight.flight_number} отменен.")
        if hasattr(flight, "load_baggage"):
            flight.load_baggage(baggage)
        baggage.check_weight()
        self._tons_loaded = round(
            self._tons_loaded + (baggage.weight_kg / self.KG_PER_TON), 3
        )

    def unload_from_cargo_hold(self, flight: Flight) -> None:
        """Выгружает багаж из грузового отсека самолета на перрон."""
        if not self.is_on_shift:
            raise ValueError(f"Грузчик {self.full_name} не на смене.")
        if flight.status == "InFlight":
            raise ValueError(f"Рейс {flight.flight_number} еще в воздухе.")
