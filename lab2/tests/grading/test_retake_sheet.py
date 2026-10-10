import pytest
from lab2.domain.academics.subject import Subject
from lab2.domain.grading.retake_sheet import RetakeSheet
from lab2.domain.people.student import Student


def test_retake_sheet():
    s = Student("A", "A")
    subj = Subject("Math", 1)
    sheet = RetakeSheet(s, subj, max_attempts=2)

    g1 = sheet.register_attempt(3)
    assert g1.score == 3
    assert sheet.attempts_used == 1
    assert sheet.is_valid is True

    g2 = sheet.register_attempt(8)
    assert g2.score == 8
    assert sheet.attempts_used == 2
    assert sheet.is_valid is False

    with pytest.raises(ValueError, match="исчерпан"):
        sheet.register_attempt(4)
