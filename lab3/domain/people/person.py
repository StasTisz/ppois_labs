from __future__ import annotations


class Person:
    def __init__(self, first_name: str, last_name: str, passport_number: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.passport_number = passport_number
        self.contact_phone = ""

    @property
    def person_id(self) -> str:
        return self.passport_number

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def change_last_name(self, new_last_name: str) -> None:
        if not new_last_name.strip():
            raise ValueError("Фамилия не может быть пустой.")
        self.last_name = new_last_name

    def update_contact(self, phone: str) -> None:
        if not phone.strip():
            raise ValueError("Номер телефона не может быть пустым.")
        self.contact_phone = phone

    def get_full_info(self) -> str:
        phone_part = f", тел: {self.contact_phone}" if self.contact_phone else ""
        return f"{self.full_name} (паспорт: {self.passport_number}{phone_part})"

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.full_name!r}, passport={self.passport_number!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.passport_number == other.passport_number

    def __hash__(self) -> int:
        return hash(self.passport_number)
