from lab2.domain.documents.academic_certificate import AcademicCertificate
from lab2.domain.people.student import Student


def test_academic_certificate():
    s = Student("С", "С")
    cert = AcademicCertificate(s, "Военкомат")
    assert cert.student == s
    assert cert.destination == "Военкомат"
    assert "Справка об обучении" in cert.title
