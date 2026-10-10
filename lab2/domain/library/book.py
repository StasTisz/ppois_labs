from __future__ import annotations

import uuid


class Book:
    """
    Учебная литература (книга в фонде библиотеки).

    Attributes:
        book_id (str): Уникальный внутренний идентификатор книги (UUID).
        title (str): Название.
        author (str): Автор.
        isbn (str): Международный стандартный книжный номер (ISBN).
        total_copies (int): Общее количество закупленных экземпляров.
        available_copies (int): Количество экземпляров, доступных для выдачи в данный момент.
    """

    def __init__(self, title: str, author: str, isbn: str, total_copies: int) -> None:
        self.book_id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = total_copies

    def borrow(self) -> None:
        """
        Списывает один экземпляр при выдаче книги читателю.

        Raises:
            ValueError: Если доступных экземпляров больше нет.
        """
        if not self.is_available:
            raise ValueError(f"Книга '{self.title}' закончилась.")
        self.available_copies -= 1

    def return_book(self) -> None:
        """
        Возвращает один экземпляр в доступный фонд.

        Raises:
            ValueError: Если библиотека уже укомплектована (защита от лишних возвратов).
        """
        if self.available_copies >= self.total_copies:
            raise ValueError("Все экземпляры уже в библиотеке.")
        self.available_copies += 1

    @property
    def is_available(self) -> bool:
        """Бизнес-правило: проверяет, доступна ли книга для выдачи."""
        return self.available_copies > 0

    @property
    def popularity_index(self) -> int:
        """Агрегация: вычисляет, сколько экземпляров сейчас находится на руках у читателей."""
        return self.total_copies - self.available_copies
