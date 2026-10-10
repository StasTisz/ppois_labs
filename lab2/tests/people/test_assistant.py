from lab2.domain.people.assistant import Assistant


def test_assistant():
    ass = Assistant("Ассистент", "Ассистентов")
    assert ass.degree == "Магистр"
    assert ass.position == "Преподаватель"
