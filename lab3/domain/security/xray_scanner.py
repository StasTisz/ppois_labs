from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.security.scanner import Scanner

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger


class XRayScanner(Scanner):
    def __init__(
        self,
        model: str,
        serial_number: str | None = None,
        contrast_level: float = 1.0,
        radiation_dose_msv: float = 0.05,
    ) -> None:
        super().__init__(model, serial_number)
        self.contrast_level = contrast_level
        self.radiation_dose_msv = radiation_dose_msv
        self.high_penetration_mode: bool = False

    def adjust_contrast(self, contrast: float) -> None:
        if contrast <= 0.0:
            raise ValueError("Контраст должен быть положительным числом.")
        self.contrast_level = contrast

    def detect_organic_materials(self, baggage: Baggage) -> bool:
        if not self.is_active:
            raise ValueError(f"Интроскоп {self.model} выключен.")
        return baggage.weight_kg > 0.0

    def scan(self, target: Passenger | Baggage | None) -> bool:
        if not self.is_active:
            raise ValueError(f"Интроскоп {self.model} выключен.")
        return True
