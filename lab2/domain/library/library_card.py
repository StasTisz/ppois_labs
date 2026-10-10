from __future__ import annotations

import uuid

from lab2.domain.library.book import Book
from lab2.domain.people.student import Student


class LibraryCard:
    """
    Читательский билет студента для учета выданной литературы.

    Attributes:
        card_id (str): Уникальный номер билета (UUID).
        student (Student): Владелец билета (студент).
    """
    MAX_BOOKS_LIMIT = 5

    def __init__(self, student: Student) -> None:
        self.card_id = str(uuid.uuid4())
        self.student = student
        self._borrowed_books: list[Book] = []
        student.library_card = self

    def take_book(self, book: Book) -> None:
        """
        Оформляет выдачу книги на данный читательский билет.

        Args:
            book (Book): Экземпляр запрашиваемой книги.

        Raises:
            ValueError: Если превышен лимит книг на руках или студент уже взял эту же книгу.
        """
        if self.borrowed_count >= self.MAX_BOOKS_LIMIT:
            raise ValueError(f"Нельзя взять более {self.MAX_BOOKS_LIMIT} книг одновременно.")

        if self.has_book(book):
            raise ValueError(f"Книга '{book.title}' уже числится за этим билетом.")

        book.borrow()
        self._borrowed_books.append(book)

    def return_book(self, book: Book) -> None:
        """
        Оформляет возврат книги в библиотеку.

        Args:
            book (Book): Возвращаемая книга.

        Raises:
            ValueError: Если эта книга не числится за данным студентом.
        """
        if not self.has_book(book):
            raise ValueError("Эта книга не числится за данным билетом.")

        book.return_book()
        self._borrowed_books.remove(book)

    @property
    def borrowed_count(self) -> int:
        """Агрегация: текущее количество книг на руках."""
        return len(self._borrowed_books)

    def has_book(self, book: Book) -> bool:
        """Проверяет, числится ли конкретная книга за этим билетом."""
        return book in self._borrowed_books
