"""Модуль аэровокзального пассажирского терминала."""

from __future__ import annotations

from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.infrastructure.check_in_counter import CheckInCounter
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.infrastructure.lounge import Lounge


class Terminal:
    """Пассажирский терминал. Агрегирует гейты, стойки, залы и карусели в единый хаб."""

    def __init__(self, name: str) -> None:
        """Инициализирует экземпляр класса Terminal."""
        self.name = name
        self._gates: list[Gate] = []
        self._check_in_counters: list[CheckInCounter] = []
        self._carousels: list[BaggageCarousel] = []
        self._lounges: list[Lounge] = []

    @property
    def gates(self) -> list[Gate]:
        """Возвращает значение атрибута gates."""
        return list(self._gates)

    @property
    def check_in_counters(self) -> list[CheckInCounter]:
        """Возвращает значение атрибута check_in_counters."""
        return list(self._check_in_counters)

    @property
    def carousels(self) -> list[BaggageCarousel]:
        """Возвращает значение атрибута carousels."""
        return list(self._carousels)

    @property
    def lounges(self) -> list[Lounge]:
        """Возвращает значение атрибута lounges."""
        return list(self._lounges)

    def add_gate(self, gate: Gate) -> None:
        """Добавляет гейт выхода на посадку в структуру терминала."""
        self._gates.append(gate)

    def add_counter(self, counter: CheckInCounter) -> None:
        """Добавляет стойку регистрации пассажиров в зале вылета."""
        self._check_in_counters.append(counter)

    def add_carousel(self, carousel: BaggageCarousel) -> None:
        """Вводит в строй багажную ленту выдачи в зоне прилета терминала."""
        self._carousels.append(carousel)

    def add_lounge(self, lounge: Lounge) -> None:
        """Открывает зал ожидания повышенной комфортности в терминале."""
        self._lounges.append(lounge)

    def get_gate(self, number: str) -> Gate | None:
        """Возвращает объект гейта по его строковому номеру (например, 'A1')."""
        for gate in self._gates:
            if gate.number == number:
                return gate
        return None

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Terminal(name={self.name!r}, gates={len(self._gates)}, counters={len(self._check_in_counters)})"
