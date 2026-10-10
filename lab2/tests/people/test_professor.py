from lab2.domain.people.professor import Professor


def test_professor():
    prof = Professor("Профессор", "Профессоров")
    assert prof.degree == "Д.т.н."
