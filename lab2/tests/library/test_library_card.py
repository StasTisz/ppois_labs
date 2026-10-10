import pytest
from lab2.domain.library.book import Book
from lab2.domain.library.library_card import LibraryCard
from lab2.domain.people.student import Student


def test_library_card():
    s = Student("А", "Б")
    card = LibraryCard(s)
    assert s.library_card == card
    assert card.borrowed_count == 0

    books = [Book(str(i), "A", f"isbn-{i}", 1) for i in range(6)]

    # 1. Берем первую книгу
    card.take_book(books[0])
    assert card.borrowed_count == 1
    assert card.has_book(books[0]) is True

    # 2. Проверяем запрет на повторную выдачу той же книги (пока лимит не исчерпан)
    with pytest.raises(ValueError, match="уже числится"):
        card.take_book(books[0])

    # 3. Добираем книги до лимита в 5 штук
    for b in books[1:5]:
        card.take_book(b)
    assert card.borrowed_count == 5

    # 4. Проверяем ошибку превышения лимита (попытка взять 6-ю книгу)
    with pytest.raises(ValueError, match="Нельзя взять более"):
        card.take_book(books[5])

    # 5. Ошибка возврата книги, которой нет на руках
    with pytest.raises(ValueError, match="не числится"):
        card.return_book(books[5])

    # 6. Успешный возврат
    card.return_book(books[0])
    assert card.borrowed_count == 4
    assert card.has_book(books[0]) is False