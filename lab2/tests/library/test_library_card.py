import pytest
from lab2.domain.exceptions import LibraryLimitExceededException
from lab2.domain.library.book import Book
from lab2.domain.library.library_card import LibraryCard
from lab2.domain.people.student import Student


def test_library_card():
    s = Student("А", "Б")
    card = LibraryCard(s)
    assert s.library_card == card
    assert card.borrowed_count == 0

    books = [Book(str(i), "A", f"isbn-{i}", 1) for i in range(6)]
    card.take_book(books[0])
    assert card.borrowed_count == 1
    assert card.has_book(books[0]) is True

    with pytest.raises(ValueError, match="уже числится"):
        card.take_book(books[0])

    for b in books[1:5]:
        card.take_book(b)
    assert card.borrowed_count == 5

    with pytest.raises(LibraryLimitExceededException):
        card.take_book(books[5])

    with pytest.raises(ValueError, match="не числится"):
        card.return_book(books[5])

    card.return_book(books[0])
    assert card.borrowed_count == 4
    assert card.has_book(books[0]) is False
