from lab3.domain.people.person import Person


def test_person():
    p = Person("Иван", "Иванов", "AB1234567")
    assert p.first_name == "Иван"
    assert p.last_name == "Иванов"
    assert p.passport_number == "AB1234567"
    assert p.full_name == "Иван Иванов"
