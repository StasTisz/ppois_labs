import pytest

from lab2.domain.exceptions import BookNotAvailableException
from lab2.domain.library.book import Book


def test_book():
    b = Book("Книга", "Автор", "123-456", 1)
    assert b.is_available is True
    assert b.popularity_index == 0
    assert "Книга" in str(b)
    assert "123-456" in repr(b)
    assert b == Book("Другая", "Другой", "123-456", 5)
    assert b != "NotABook"
    assert len({b, Book("Клон", "Клон", "123-456", 2)}) == 1

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

    b.add_copies(3)
    assert b.total_copies == 4
    assert b.available_copies == 4

    with pytest.raises(ValueError):
        b.add_copies(0)
