from __future__ import annotations

from lab3.domain.people.employee import Employee


class BaggageHandler(Employee):
    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, heavy_machinery_license: bool
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.heavy_machinery_license = heavy_machinery_license
        self._tons_loaded = 0.0

    @property
    def tons_loaded(self) -> float:
        return self._tons_loaded

    def perform_duty(self) -> str:
        self._tons_loaded += 0.5
        equipment = "с помощью погрузчика" if self.heavy_machinery_license else "вручную"
        return f"Грузчик {self.full_name} переместил багаж {equipment}."
