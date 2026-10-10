import pytest
from lab2.domain.people.lecturer import Lecturer


def test_lecturer():
    lec = Lecturer("Лектор", "Лекторов")
    assert lec.subjects_count == 0

    lec.assign_subject("Математика")
    lec.assign_subject("Математика")
    assert lec.subjects_count == 1
    assert lec.can_teach("Математика") is True
    assert lec.can_teach("Физика") is False

    lec.update_degree("К.ф.-м.н.")
    assert lec.degree == "К.ф.-м.н."

    with pytest.raises(ValueError):
        lec.update_degree("")
    with pytest.raises(ValueError):
        lec.update_degree("   ")
