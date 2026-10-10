import pytest
from lab2.domain.academics.subject import Subject
from lab2.domain.exceptions import InvalidScoreException
from lab2.domain.grading.grade import Grade


def test_grade():
    subj = Subject("ООП", 1)
    g1 = Grade(subj, 8, is_exam=True)
    assert g1.subject == subj
    assert g1.subject_name == "ООП"
    assert g1.score == 8
    assert g1.is_exam is True
    assert g1.is_passed is True

    g2 = Grade("Физика", 3, is_exam=False)
    assert g2.subject_name == "Физика"
    assert g2.is_passed is False

    with pytest.raises(InvalidScoreException):
        Grade("Химия", -1)
    with pytest.raises(InvalidScoreException):
        Grade("Химия", 11)
