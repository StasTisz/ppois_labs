"""Модуль посадочного талона пассажира."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.operations.ticket import Ticket

if TYPE_CHECKING:
    from lab3.domain.infrastructure.gate import Gate


class BoardingPass:
    """Посадочный талон, выдаваемый после успешной регистрации и сдачи багажа."""

    _pass_counter: int = 200000

    def __init__(
        self,
        ticket: Ticket,
        seat_number: str,
        gate: Gate | None = None,
        pass_id: str | None = None,
    ) -> None:
        """Инициализирует экземпляр класса BoardingPass."""
        BoardingPass._pass_counter += 1
        self.pass_id = pass_id or f"BP-{BoardingPass._pass_counter}"
        self.ticket = ticket
        self.seat_number = seat_number
        self.gate: Gate | None = gate
        self._is_boarded = False

    @property
    def gate_number(self) -> str:
        """Возвращает значение атрибута gate_number."""
        if self.gate is not None:
            return self.gate.number
        return "TBD"

    @property
    def is_boarded(self) -> bool:
        """Возвращает признак boarded."""
        return self._is_boarded

    def mark_boarded(self) -> None:
        """Отмечает факт успешной посадки пассажира на борт воздушного судна."""
        self._is_boarded = True

    def verify_gate(self, current_gate: Gate) -> bool:
        """Сверяет номер выхода на посадку с назначенным в посадочном талоне."""
        if self.gate is None:
            return False
        return self.gate == current_gate

    def change_seat(self, new_seat: str) -> None:
        """Изменяет назначенное посадочное место пассажира."""
        if self._is_boarded:
            raise ValueError("Нельзя изменить место: посадка уже завершена.")
        self.seat_number = new_seat

    def assign_gate(self, gate: Gate) -> None:
        """Назначает гейт выхода на посадку для данного талона."""
        self.gate = gate

    def get_summary(self) -> str:
        """Формирует краткую сводку данных посадочного талона."""
        return (
            f"Pass #{self.pass_id}: Seat {self.seat_number}, Gate {self.gate_number}, "
            f"Boarded: {self._is_boarded}"
        )

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"BoardingPass(ticket={self.ticket!r}, seat={self.seat_number!r}, gate={self.gate_number!r})"
