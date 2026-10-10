from __future__ import annotations


class Timeslot:
    """
    Временной слот для проведения занятия (пара).

    Attributes:
        sequence_number (int): Порядковый номер пары в расписании (1, 2, 3...).
        start_time (str): Время начала в формате "HH:MM".
        end_time (str): Время окончания в формате "HH:MM".
    """

    def __init__(self, sequence_number: int, start_time: str, end_time: str) -> None:
        self.sequence_number = sequence_number
        self.start_time = start_time
        self.end_time = end_time

    @property
    def duration_minutes(self) -> int:
        """Агрегация: вычисляет продолжительность занятия в минутах."""
        start_h, start_m = map(int, self.start_time.split(':'))
        end_h, end_m = map(int, self.end_time.split(':'))
        return (end_h * 60 + end_m) - (start_h * 60 + start_m)
