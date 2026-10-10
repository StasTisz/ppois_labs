import pytest
from lab2.domain.academics.subject import Subject
from lab2.domain.grading.grade import Grade
from lab2.domain.grading.record_book import RecordBook
from lab2.domain.people.student import Student


def test_record_book():
    s = Student("С", "С")
    rb = RecordBook(s, "ZK-1")
    assert rb.student == s
    assert rb.student_id == s.person_id
    assert s.record_book == rb
    assert rb.average_score == 0.0
    assert rb.get_best_subject() is None
    assert rb.is_excellent is False

    rb.add_grade(Grade("ООП", 9, is_exam=True))
    with pytest.raises(ValueError, match="уже стоит"):
        rb.add_grade(Grade("ООП", 10, is_exam=True))

    rb.add_grade(Grade("Физика", 3, is_exam=True))
    assert rb.average_score == 6.0
    assert rb.is_excellent is False
    assert rb.get_best_subject() == "ООП"

    debts = rb.get_debts()
    assert "Физика" in debts
    rb.clear_debts_for_subject("Физика")
    assert len(rb.get_debts()) == 0

    subj = Subject("Математика", 1)
    rb.add_grade(Grade(subj, 2, is_exam=False))
    rb.clear_debts_for_subject(subj)
    assert len(rb.get_debts()) == 0

    rb2 = RecordBook("str-id", "ZK-2")
    assert rb2.student_id == "str-id"
