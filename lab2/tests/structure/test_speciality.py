import pytest

from lab2.domain.structure.speciality import Speciality


def test_speciality():
    spec = Speciality("ИИ", "Искусственный интеллект")
    assert str(spec) == "[ИИ] Искусственный интеллект"
    assert spec.semesters_count == 8
    assert spec.is_bachelor() is True
    assert "Speciality" in repr(spec)
    assert spec == Speciality("ИИ", "Другое имя")
    assert spec != "NotASpeciality"
    assert len({spec, Speciality("ИИ", "Искусственный интеллект")}) == 1

    spec.update_semesters_count(10)
    assert spec.semesters_count == 10
    assert spec.is_bachelor() is False

    with pytest.raises(ValueError):
        spec.update_semesters_count(1)
    with pytest.raises(ValueError):
        spec.update_semesters_count(13)

    spec.rename("Интеллектуальные системы")
    assert spec.name == "Интеллектуальные системы"

    with pytest.raises(ValueError):
        spec.rename("   ")
