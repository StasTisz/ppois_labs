from __future__ import annotations

import uuid


class Person:
    def __init__(self, first_name: str, last_name: str, passport_number: str) -> None:
        self.person_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.passport_number = passport_number

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
