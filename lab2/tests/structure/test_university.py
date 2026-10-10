import pytest
from lab2.domain.structure.faculty import Faculty
from lab2.domain.structure.university import University


def test_university():
    u = University("БГУИР", "БГУИР")
    f = Faculty("ФИТиУ", "ФИТиУ")
    u.add_faculty(f)

    with pytest.raises(ValueError):
        u.add_faculty(f)

    assert u.find_faculty("ФИТиУ") == f
    assert u.find_faculty("Неизвестный") is None
