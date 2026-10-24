"""Модуль временного интервала (таймслота) занятий."""

from __future__ import annotations


class Timeslot:
    """Временной слот для проведения занятия (пара)."""

    MINUTES_PER_HOUR: int = 60

    def __init__(self, sequence_number: int, start_time: str, end_time: str) -> None:
        """Инициализирует экземпляр класса Timeslot."""
        self.sequence_number = sequence_number
        self.start_time = start_time
        self.end_time = end_time

    @property
    def duration_minutes(self) -> int:
        """Агрегация: вычисляет продолжительность занятия в минутах."""
        start_h, start_m = map(int, self.start_time.split(":"))
        end_h, end_m = map(int, self.end_time.split(":"))
        return (end_h * self.MINUTES_PER_HOUR + end_m) - (
            start_h * self.MINUTES_PER_HOUR + start_m
        )

    def conflicts_with(self, other: Timeslot) -> bool:
        """Проверяет наличие пересечения по времени с другим таймслотом."""
        if self.sequence_number == other.sequence_number:
            return True
        return self.start_time == other.start_time and self.end_time == other.end_time

    def format_timeslot(self) -> str:
        """Форматирует границы таймслота в человекочитаемую строку."""
        return f"Пара #{self.sequence_number} ({self.start_time} - {self.end_time})"

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return (
            f"Timeslot(seq={self.sequence_number}, {self.start_time}-{self.end_time})"
        )

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Timeslot):
            return NotImplemented
        return self.sequence_number == other.sequence_number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.sequence_number)
