import pytest
from lab2.domain.exceptions import BookNotAvailableException
from lab2.domain.library.book import Book


def test_book():
    b = Book("Книга", "Автор", "123-456", 1)
    assert b.is_available is True
    assert b.popularity_index == 0

    b.borrow()
    assert b.is_available is False
    assert b.popularity_index == 1

    with pytest.raises(BookNotAvailableException):
        b.borrow()

    b.return_book()
    assert b.is_available is True
    assert b.popularity_index == 0

    with pytest.raises(ValueError):
        b.return_book()
