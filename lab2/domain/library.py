import uuid

from lab2.domain.people import Student


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

        # Добавлено бизнес-правило: нельзя взять две одинаковые книги на один билет
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