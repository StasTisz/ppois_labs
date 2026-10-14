import pytest

from lab2.domain.people.professor import Professor
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_professor():
    prof = Professor("Профессор", "Профессоров")
    assert prof.degree == "Д.т.н."

    s = Student("Студент", "Студентов")
    msg1 = prof.supervise_graduate(s, "Нейросетевые методы анализа кода")
    assert "утвержден научным руководителем" in msg1

    s.expel()
    with pytest.raises(ValueError, match="отчисленного"):
        prof.supervise_graduate(s, "Любая тема")

    group = AcademicGroup("101", Speciality("ПОИТ", "POIT-01"))
    msg2 = prof.chair_defense_committee(group)
    assert "возглавил государственную" in msg2

    msg3 = prof.conduct_scientific_seminar("Квантовые алгоритмы")
    assert "научный семинар" in msg3

    with pytest.raises(ValueError):
        prof.conduct_scientific_seminar("   ")
