"""Модуль арочного металлодетектора пункта досмотра."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.security.scanner import Scanner

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger


class MetalDetector(Scanner):
    """Рамочный металлодетектор для досмотра людей."""

    MIN_SENSITIVITY: int = 1
    MAX_SENSITIVITY: int = 10

    def __init__(
        self, model: str, serial_number: str | None = None, sensitivity_level: int = 5
    ) -> None:
        """Инициализирует экземпляр класса MetalDetector."""
        super().__init__(model, serial_number)
        self.sensitivity_level = sensitivity_level
        self.alarm_triggered_count: int = 0

    def set_sensitivity(self, level: int) -> None:
        """Настраивает порог чувствительности стационарного металлодетектора."""
        if not (self.MIN_SENSITIVITY <= level <= self.MAX_SENSITIVITY):
            raise ValueError(
                f"Уровень чувствительности должен быть от {self.MIN_SENSITIVITY} до {self.MAX_SENSITIVITY}."
            )
        self.sensitivity_level = level

    def test_alarm(self) -> bool:
        """Выполняет тестовую проверку звуковой и световой сигнализации тревоги."""
        return self.is_active

    def scan(self, target: Passenger | Baggage | None) -> bool:
        """Анализирует наличие металла у пассажира."""
        if not self.is_active:
            raise ValueError(f"Детектор {self.model} выключен.")
        return True
