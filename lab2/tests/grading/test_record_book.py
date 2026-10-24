import pytest

from lab2.domain.academics.subject import Subject
from lab2.domain.grading.grade import Grade
from lab2.domain.grading.record_book import RecordBook
from lab2.domain.people.student import Student


def test_record_book():
    s = Student("С", "С")
    rb = RecordBook(s, "ZK-1")
    assert rb.student == s
    assert s.record_book == rb
    assert rb.average_score == 0.0
    assert rb.get_best_subject() is None
    assert rb.is_excellent is False

    oop_subj = Subject("ООП", 1)
    phys_subj = Subject("Физика", 1)
    math_subj = Subject("Математика", 1)

    rb.add_grade(Grade(oop_subj, 9, is_exam=True))
    with pytest.raises(ValueError, match="уже стоит"):
        rb.add_grade(Grade(oop_subj, 10, is_exam=True))

    rb.add_grade(Grade(phys_subj, 3, is_exam=True))
    assert rb.average_score == 6.0
    assert rb.is_excellent is False
    assert rb.get_best_subject() == oop_subj.name

    debts = rb.get_debts()
    assert phys_subj.name in debts
    rb.clear_debts_for_subject(phys_subj)
    assert len(rb.get_debts()) == 0

    rb.add_grade(Grade(math_subj, 2, is_exam=False))
    rb.clear_debts_for_subject(math_subj)
    assert len(rb.get_debts()) == 0

    s2 = Student("Б", "Б")
    rb2 = RecordBook(s2, "ZK-2")
    assert rb2.student == s2
