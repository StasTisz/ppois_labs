from __future__ import annotations

import uuid
from typing import Any


class Person:
    def __init__(self, first_name: str, last_name: str, middle_name: str = "") -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.person_id = str(uuid.uuid4())
        self.bank_account: Any = None

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    def __str__(self) -> str:
        return self.full_name

    def change_last_name(self, new_last_name: str) -> None:
        if not new_last_name.strip():
            raise ValueError("Фамилия не может быть пустой.")
        self.last_name = new_last_name
