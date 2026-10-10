from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import SecurityCheckFailedException

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger
    from lab3.domain.people.security_officer import SecurityOfficer
    from lab3.domain.security.metal_detector import MetalDetector
    from lab3.domain.security.xray_scanner import XRayScanner


class SecurityCheckpoint:
    def __init__(self, number: int) -> None:
        self.checkpoint_id = str(uuid.uuid4())
        self.number = number
        self.metal_detector: MetalDetector | None = None
        self.xray_scanner: XRayScanner | None = None
        self.officer: SecurityOfficer | None = None

    def assign_equipment(self, metal_detector: MetalDetector, xray_scanner: XRayScanner) -> None:
        self.metal_detector = metal_detector
        self.xray_scanner = xray_scanner

    def assign_officer(self, officer: SecurityOfficer) -> None:
        self.officer = officer

    def process_passenger(self, passenger: Passenger, carry_on: Baggage | None = None) -> None:
        if not self.metal_detector or not self.xray_scanner:
            raise ValueError(f"Пункт досмотра {self.number} не укомплектован оборудованием.")
        if not self.officer or not self.officer.is_on_shift:
            raise ValueError("Нет дежурного офицера для проведения досмотра.")

        person_clear = self.metal_detector.scan(passenger)
        baggage_clear = self.xray_scanner.scan(carry_on) if carry_on else True

        if not person_clear or not baggage_clear:
            raise SecurityCheckFailedException(f"Пассажир {passenger.full_name} не прошел досмотр СБ.")
