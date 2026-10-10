import pytest
from lab2.domain.academics.labwork import LabWork
from lab2.domain.academics.subject import Subject


def test_subject():
    lab1 = LabWork("Лаб 1", 10.0)
    lab2 = LabWork("Лаб 2", 15.0)
    lab2.make_optional()

    subj = Subject("ООП", 2)
    subj.add_lab(lab1)
    subj.add_lab(lab2)
    assert lab1.subject == subj

    with pytest.raises(ValueError):
        subj.add_lab(LabWork("Лаб 1"))
    with pytest.raises(ValueError):
        subj.remove_lab("Несуществующая лаба")

    assert subj.total_mandatory_labs == 1
    assert len(subj.get_mandatory_labs()) == 1
    assert subj.max_possible_score == 25.0

    subj.remove_lab("Лаб 1")
    assert len(subj._labs) == 1
