from lab2.domain.people.associate_professor import AssociateProfessor


def test_associate_professor():
    ap = AssociateProfessor("Доцент", "Доцентов")
    assert ap.degree == "К.т.н."
