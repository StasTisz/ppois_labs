"""Модуль библиотечной книги фонда университета."""

from __future__ import annotations

from lab2.domain.exceptions import BookNotAvailableException


class Book:
    """Учебная литература (книга в фонде библиотеки)."""

    def __init__(self, title: str, author: str, isbn: str, total_copies: int) -> None:
        """Инициализирует экземпляр класса Book."""
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self._available_copies = total_copies

    @property
    def available_copies(self) -> int:
        """Возвращает значение атрибута available_copies."""
        return self._available_copies

    def borrow(self) -> None:
        """Списывает один экземпляр при выдаче книги читателю."""
        if not self.is_available:
            raise BookNotAvailableException(f"Книга '{self.title}' закончилась.")
        self._available_copies -= 1

    def return_book(self) -> None:
        """Возвращает один экземпляр в доступный фонд."""
        if self._available_copies >= self.total_copies:
            raise ValueError("Все экземпляры уже в библиотеке.")
        self._available_copies += 1

    def add_copies(self, count: int) -> None:
        """Пополняет библиотечный фонд дополнительными экземплярами книги."""
        if count <= 0:
            raise ValueError(
                "Количество добавляемых экземпляров должно быть положительным."
            )
        self.total_copies += count
        self._available_copies += count

    @property
    def is_available(self) -> bool:
        """Бизнес-правило: проверяет, доступна ли книга для выдачи."""
        return self._available_copies > 0

    @property
    def popularity_index(self) -> int:
        """Агрегация: вычисляет, сколько экземпляров сейчас находится на руках у читателей."""
        return self.total_copies - self._available_copies

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return f"'{self.title}' ({self.author}) [ISBN: {self.isbn}]"

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Book(isbn={self.isbn!r}, title={self.title!r}, copies={self._available_copies}/{self.total_copies})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Book):
            return NotImplemented
        return self.isbn == other.isbn

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.isbn)
