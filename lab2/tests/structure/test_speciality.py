import pytest
from lab2.domain.structure.speciality import Speciality


def test_speciality():
    spec = Speciality("ИИ", "Искусственный интеллект")
    assert str(spec) == "[ИИ] Искусственный интеллект"
    assert spec.semesters_count == 8

    spec.update_semesters_count(10)
    assert spec.semesters_count == 10

    with pytest.raises(ValueError):
        spec.update_semesters_count(1)
    with pytest.raises(ValueError):
        spec.update_semesters_count(13)
