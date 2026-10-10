import pytest
from lab2.domain.academics.labwork import LabWork


def test_labwork():
    lab1 = LabWork("Лаб 1", 10.0)
    lab2 = LabWork("Лаб 2", 15.0)

    assert "Обязательная" in lab1.short_info
    lab2.make_optional()
    assert "Бонусная" in lab2.short_info

    lab1.update_score_limit(20.0)
    with pytest.raises(ValueError):
        lab1.update_score_limit(-5.0)
    with pytest.raises(ValueError):
        lab1.update_score_limit(0)
