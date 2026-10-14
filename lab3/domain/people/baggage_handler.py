from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight import Flight


class BaggageHandler(Employee):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        heavy_machinery_license: bool = True,
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.heavy_machinery_license = heavy_machinery_license
        self._tons_loaded = 0.0

    @property
    def tons_loaded(self) -> float:
        return self._tons_loaded

    def perform_duty(self) -> str:
        if self.heavy_machinery_license:
            self._tons_loaded += 2.0
            return f"Грузчик {self.full_name} загружает багаж с помощью погрузчика."
        self._tons_loaded += 0.5
        return f"Грузчик {self.full_name} загружает багаж вручную."

    def load_to_cargo_hold(self, flight: Flight, baggage: Baggage) -> None:
        if not self.is_on_shift:
            raise ValueError(f"Грузчик {self.full_name} не на смене.")
        baggage.check_weight()
        self._tons_loaded = round(self._tons_loaded + (baggage.weight_kg / 1000.0), 3)

    def unload_from_cargo_hold(self, flight: Flight) -> None:
        if not self.is_on_shift:
            raise ValueError(f"Грузчик {self.full_name} не на смене.")
