"""Модуль пункта предполетного досмотра пассажиров."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import SecurityCheckFailedException

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger
    from lab3.domain.people.security_officer import SecurityOfficer
    from lab3.domain.security.metal_detector import MetalDetector
    from lab3.domain.security.xray_scanner import XRayScanner


class SecurityCheckpoint:
    """Зона предполетного досмотра (САБ - служба авиационной безопасности)."""

    def __init__(self, number: int) -> None:
        """Инициализирует экземпляр класса SecurityCheckpoint."""
        self.number = number
        self.metal_detector: MetalDetector | None = None
        self.xray_scanner: XRayScanner | None = None
        self.officer: SecurityOfficer | None = None
        self._processed_passengers_count = 0
        self._is_open = True

    @property
    def checkpoint_id(self) -> str:
        """Возвращает значение атрибута checkpoint_id."""
        return f"CP-{self.number}"

    @property
    def processed_passengers_count(self) -> int:
        """Возвращает значение атрибута processed_passengers_count."""
        return self._processed_passengers_count

    @property
    def is_open(self) -> bool:
        """Возвращает признак open."""
        return self._is_open

    def is_ready_for_service(self) -> bool:
        """Проверяет готовность пункта досмотра к обслуживанию пассажиропотока."""
        return (
            self._is_open
            and self.metal_detector is not None
            and self.metal_detector.is_active
            and self.xray_scanner is not None
            and self.xray_scanner.is_active
            and self.officer is not None
            and self.officer.is_on_shift
        )

    def close_checkpoint(self) -> None:
        """Временно закрывает пункт досмотра на технический перерыв."""
        self._is_open = False

    def open_checkpoint(self) -> None:
        """Открывает пункт досмотра для прохождения предполетного контроля."""
        self._is_open = True

    def assign_equipment(
        self, metal_detector: MetalDetector, xray_scanner: XRayScanner
    ) -> None:
        """Комплектует пункт досмотра необходимым оборудованием."""
        self.metal_detector = metal_detector
        self.xray_scanner = xray_scanner

    def assign_officer(self, officer: SecurityOfficer) -> None:
        """Назначает дежурного сотрудника на пункт."""
        self.officer = officer

    def _validate_readiness(self) -> None:
        """Проверяет работоспособность всех сканеров и присутствие офицера безопасности."""
        if not self._is_open:
            raise ValueError(f"Пункт досмотра {self.number} закрыт.")
        if not self.metal_detector or not self.xray_scanner:
            raise ValueError(
                f"Пункт досмотра {self.number} не укомплектован оборудованием."
            )
        if not self.officer or not self.officer.is_on_shift:
            raise ValueError("Нет дежурного офицера для проведения досмотра.")

    def process_passenger(
        self, passenger: Passenger, carry_on: Baggage | None = None
    ) -> None:
        """Осуществляет комплексный досмотр пассажира и его ручной клади."""
        self._validate_readiness()
        assert self.metal_detector and self.xray_scanner
        person_clear = self.metal_detector.scan(passenger)
        baggage_clear = self.xray_scanner.scan(carry_on) if carry_on else True

        if not person_clear or not baggage_clear:
            raise SecurityCheckFailedException(
                f"Пассажир {passenger.full_name} не прошел досмотр СБ."
            )
        self._processed_passengers_count += 1

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return (
            f"SecurityCheckpoint(number={self.number}, open={self._is_open}, "
            f"processed={self._processed_passengers_count})"
        )
