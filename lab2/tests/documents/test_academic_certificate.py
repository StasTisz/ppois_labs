import pytest

from lab2.domain.documents.academic_certificate import AcademicCertificate
from lab2.domain.exceptions import DocumentNotSignedException
from lab2.domain.people.dean import Dean
from lab2.domain.people.student import Student


def test_academic_certificate():
    s = Student("С", "С")
    cert = AcademicCertificate(s, "Военкомат")
    assert cert.student == s
    assert cert.destination == "Военкомат"
    assert "Справка об обучении" in cert.title
    assert cert.verify_student_status() is True
    assert "действительно является студентом" in cert.generate_text()

    with pytest.raises(DocumentNotSignedException):
        cert.issue()

    dean = Dean("Декан", "Деканов")
    cert.sign(dean)
    issued_text = cert.issue()
    assert "Военкомат" in issued_text

    s.expel()
    with pytest.raises(ValueError, match="отчисленному"):
        cert.issue()
