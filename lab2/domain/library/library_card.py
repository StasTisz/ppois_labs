from __future__ import annotations

import uuid

from lab2.domain.exceptions import LibraryLimitExceededException
from lab2.domain.library.book import Book
from lab2.domain.people.student import Student


class LibraryCard:
    MAX_BOOKS_LIMIT = 5

    def __init__(self, student: Student) -> None:
        self.card_id = str(uuid.uuid4())
        self.student = student
        self._borrowed_books: list[Book] = []
        student.library_card = self

    def take_book(self, book: Book) -> None:
        if self.has_book(book):
            raise ValueError(f"Книга '{book.title}' уже числится за этим билетом.")
        if self.borrowed_count >= self.MAX_BOOKS_LIMIT:
            raise LibraryLimitExceededException(f"Нельзя взять более {self.MAX_BOOKS_LIMIT} книг одновременно.")
        book.borrow()
        self._borrowed_books.append(book)

    def return_book(self, book: Book) -> None:
        if not self.has_book(book):
            raise ValueError("Эта книга не числится за данным билетом.")
        book.return_book()
        self._borrowed_books.remove(book)

    @property
    def borrowed_count(self) -> int:
        return len(self._borrowed_books)

    def has_book(self, book: Book) -> bool:
        return book in self._borrowed_books
