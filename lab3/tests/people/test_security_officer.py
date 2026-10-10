from lab3.domain.people.security_officer import SecurityOfficer


def test_security_officer():
    so = SecurityOfficer("Виктор", "В", "P-333", 1400.0)
    assert "досмотр" in so.perform_duty()
