"""Модуль базовой сущности физического лица."""

from __future__ import annotations


class Person:
    """Базовый класс для всех физических лиц в системе."""

    def __init__(self, first_name: str, last_name: str, passport_number: str) -> None:
        """Инициализирует экземпляр класса Person."""
        self.first_name = first_name
        self.last_name = last_name
        self.passport_number = passport_number
        self.contact_phone = ""

    @property
    def person_id(self) -> str:
        """Возвращает значение атрибута person_id."""
        return self.passport_number

    @property
    def full_name(self) -> str:
        """Возвращает полное имя персоны (Имя + Фамилия)."""
        return f"{self.first_name} {self.last_name}"

    def change_last_name(self, new_last_name: str) -> None:
        """Изменяет фамилию человека (например, при вступлении в брак)."""
        if not new_last_name.strip():
            raise ValueError("Фамилия не может быть пустой.")
        self.last_name = new_last_name

    def update_contact(self, phone: str) -> None:
        """Обновляет контактные данные (номер телефона) физического лица."""
        if not phone.strip():
            raise ValueError("Номер телефона не может быть пустым.")
        self.contact_phone = phone

    def get_full_info(self) -> str:
        """Возвращает полную персональную информацию о человеке."""
        phone_part = f", тел: {self.contact_phone}" if self.contact_phone else ""
        return f"{self.full_name} (паспорт: {self.passport_number}{phone_part})"

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return self.full_name

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"{self.__class__.__name__}({self.full_name!r}, passport={self.passport_number!r})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.passport_number == other.passport_number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.passport_number)
