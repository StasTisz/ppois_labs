"""Модуль рентгенотелевизионного интроскопа для багажа."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.security.scanner import Scanner

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger


class XRayScanner(Scanner):
    """Рентгеновский интроскоп для досмотра ручной клади и багажа."""

    def __init__(
        self,
        model: str,
        serial_number: str | None = None,
        contrast_level: float = 1.0,
        radiation_dose_msv: float = 0.05,
    ) -> None:
        """Инициализирует экземпляр класса XRayScanner."""
        super().__init__(model, serial_number)
        self.contrast_level = contrast_level
        self.radiation_dose_msv = radiation_dose_msv
        self.high_penetration_mode: bool = False

    def adjust_contrast(self, contrast: float) -> None:
        """Регулирует контрастность рентгеновского снимка багажа."""
        if contrast <= 0.0:
            raise ValueError("Контраст должен быть положительным числом.")
        self.contrast_level = contrast

    def detect_organic_materials(self, baggage: Baggage) -> bool:
        """Анализирует снимок на наличие запрещенных органических соединений."""
        if not self.is_active:
            raise ValueError(f"Интроскоп {self.model} выключен.")
        return baggage.weight_kg > 0.0

    def scan(self, target: Passenger | Baggage | None) -> bool:
        """Просвечивает багаж на наличие запрещенных к перевозке веществ."""
        if not self.is_active:
            raise ValueError(f"Интроскоп {self.model} выключен.")
        return True
