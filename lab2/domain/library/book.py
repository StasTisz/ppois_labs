from __future__ import annotations

import uuid


class Book:
    def __init__(self, title: str, author: str, isbn: str, total_copies: int) -> None:
        self.book_id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = total_copies

    def borrow(self) -> None:
        if not self.is_available:
            raise ValueError(f"Книга '{self.title}' закончилась.")
        self.available_copies -= 1

    def return_book(self) -> None:
        if self.available_copies >= self.total_copies:
            raise ValueError("Все экземпляры уже в библиотеке.")
        self.available_copies += 1

    @property
    def is_available(self) -> bool:
        return self.available_copies > 0

    @property
    def popularity_index(self) -> int:
        return self.total_copies - self.available_copies
