import uuid
from typing import List, Optional
from lab2.domain.people import Student

class Book:
    """Учебная литература."""
    def __init__(self, title: str, author: str, isbn: str, total_copies: int):
        self.book_id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = total_copies

    def borrow(self):
        if self.available_copies <= 0:
            raise ValueError(f"Книга '{self.title}' закончилась.")
        self.available_copies -= 1

    def return_book(self):
        if self.available_copies >= self.total_copies:
            raise ValueError("Все экземпляры уже в библиотеке.")
        self.available_copies += 1

    @property
    def is_available(self) -> bool:
        """Бизнес-свойство: доступна ли книга для выдачи."""
        return self.available_copies > 0

    @property
    def popularity_index(self) -> int:
        """Бизнес-свойство: сколько экземпляров сейчас на руках у читателей."""
        return self.total_copies - self.available_copies


class LibraryCard:
    """Читательский билет студента."""
    def __init__(self, student: Student):
        self.card_id = str(uuid.uuid4())
        self.student = student
        self._borrowed_books: List[Book] = []

    def take_book(self, book: Book):
        if len(self._borrowed_books) >= 5:
            raise ValueError("Нельзя взять более 5 книг одновременно.")
        book.borrow()
        self._borrowed_books.append(book)

    def return_book(self, book: Book):
        if book not in self._borrowed_books:
            raise ValueError("Эта книга не числится за данным билетом.")
        book.return_book()
        self._borrowed_books.remove(book)

    @property
    def borrowed_count(self) -> int:
        """Свойство: текущее количество взятых книг."""
        return len(self._borrowed_books)

    def has_book(self, book: 'Book') -> bool:
        """Проверка: числится ли конкретная книга за этим студентом."""
        return book in self._borrowed_books