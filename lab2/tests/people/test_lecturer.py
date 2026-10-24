import pytest

from lab2.domain.academics.subject import Subject
from lab2.domain.people.lecturer import Lecturer


def test_lecturer():
    lec = Lecturer("Лектор", "Лекторов")
    assert lec.subjects_count == 0

    math_subj = Subject("Математика", 1)
    phys_subj = Subject("Физика", 1)

    lec.assign_subject(math_subj)
    lec.assign_subject(math_subj)
    assert lec.subjects_count == 1
    assert lec.can_teach(math_subj) is True
    assert lec.can_teach(phys_subj) is False

    lec.update_degree("К.ф.-м.н.")
    assert lec.degree == "К.ф.-м.н."

    with pytest.raises(ValueError):
        lec.update_degree("")
    with pytest.raises(ValueError):
        lec.update_degree("   ")
