import pytest

from lab3.domain.people.person import Person


def test_person():
    p = Person("Иван", "Иванов", "AB1234567")
    assert p.first_name == "Иван"
    assert p.last_name == "Иванов"
    assert p.passport_number == "AB1234567"
    assert p.person_id == "AB1234567"
    assert p.full_name == "Иван Иванов"
    assert str(p) == "Иван Иванов"
    assert "Person" in repr(p)
    assert p == Person("Иван", "Иванов", "AB1234567")
    assert p != "NotAPerson"
    assert len({p, Person("Другой", "Другой", "AB1234567")}) == 1

    p.change_last_name("Петров")
    assert p.last_name == "Петров"
    with pytest.raises(ValueError):
        p.change_last_name("   ")

    p.update_contact("+375291234567")
    assert p.contact_phone == "+375291234567"
    assert "+375291234567" in p.get_full_info()

    with pytest.raises(ValueError):
        p.update_contact("   ")
