from __future__ import annotations


class Timeslot:
    def __init__(self, sequence_number: int, start_time: str, end_time: str) -> None:
        self.sequence_number = sequence_number
        self.start_time = start_time
        self.end_time = end_time

    @property
    def duration_minutes(self) -> int:
        start_h, start_m = map(int, self.start_time.split(':'))
        end_h, end_m = map(int, self.end_time.split(':'))
        return (end_h * 60 + end_m) - (start_h * 60 + start_m)
