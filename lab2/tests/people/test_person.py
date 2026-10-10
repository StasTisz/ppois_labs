import pytest
from lab2.domain.people.person import Person


def test_person():
    p = Person("Иван", "Иванов", "Иванович")
    assert p.full_name == "Иванов Иван Иванович"
    assert str(p) == "Иванов Иван Иванович"

    p.change_last_name("Петров")
    assert p.full_name == "Петров Иван Иванович"
    with pytest.raises(ValueError):
        p.change_last_name("")
    with pytest.raises(ValueError):
        p.change_last_name("   ")

    p2 = Person("Петр", "Сидоров")
    assert p2.full_name == "Сидоров Петр"
