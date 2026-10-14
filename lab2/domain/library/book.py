from __future__ import annotations

from lab2.domain.exceptions import BookNotAvailableException


class Book:
    def __init__(self, title: str, author: str, isbn: str, total_copies: int) -> None:
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self._available_copies = total_copies

    @property
    def available_copies(self) -> int:
        return self._available_copies

    def borrow(self) -> None:
        if not self.is_available:
            raise BookNotAvailableException(f"Книга '{self.title}' закончилась.")
        self._available_copies -= 1

    def return_book(self) -> None:
        if self._available_copies >= self.total_copies:
            raise ValueError("Все экземпляры уже в библиотеке.")
        self._available_copies += 1

    def add_copies(self, count: int) -> None:
        if count <= 0:
            raise ValueError(
                "Количество добавляемых экземпляров должно быть положительным."
            )
        self.total_copies += count
        self._available_copies += count

    @property
    def is_available(self) -> bool:
        return self._available_copies > 0

    @property
    def popularity_index(self) -> int:
        return self.total_copies - self._available_copies

    def __str__(self) -> str:
        return f"'{self.title}' ({self.author}) [ISBN: {self.isbn}]"

    def __repr__(self) -> str:
        return f"Book(isbn={self.isbn!r}, title={self.title!r}, copies={self._available_copies}/{self.total_copies})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.isbn == other.isbn

    def __hash__(self) -> int:
        return hash(self.isbn)
