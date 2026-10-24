"""Модуль члена летного или кабинного экипажа."""

from __future__ import annotations

from abc import ABC

from lab3.domain.people.employee import Employee


class CrewMember(Employee, ABC):
    """Абстрактный класс летного состава (экипажа).
    Вводит контроль санитарной нормы часов налета."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        max_monthly_hours: int = 90,
    ) -> None:
        """Инициализирует экземпляр класса CrewMember."""
        super().__init__(first_name, last_name, passport_number, salary)
        self.max_monthly_hours = max_monthly_hours
        self._flight_hours = 0

    @property
    def flight_hours(self) -> int:
        """Текущее количество часов налета за месяц."""
        return self._flight_hours

    def log_flight_hours(self, hours: int) -> None:
        """Фиксирует часы в рейсе."""
        if hours < 0:
            raise ValueError("Количество часов налета не может быть отрицательным.")
        if self._flight_hours + hours > self.max_monthly_hours:
            raise ValueError(
                f"Превышена санитарная норма налета ({self.max_monthly_hours} ч.)"
            )
        self._flight_hours += hours

    def reset_monthly_hours(self) -> None:
        """Сбрасывает счетчик налета часов за текущий расчетный месяц."""
        self._flight_hours = 0

    def can_fly(self, hours: int) -> bool:
        """Проверяет допуск члена экипажа к полетам по лимиту санитарных норм налета."""
        return self._flight_hours + hours <= self.max_monthly_hours
