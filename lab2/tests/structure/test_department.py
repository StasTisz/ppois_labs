import pytest
from lab2.domain.people.lecturer import Lecturer
from lab2.domain.structure.department import Department


def test_department():
    dept = Department("Кафедра ИТ")
    dept.assign_head("Шеф")
    assert dept.head_name == "Шеф"

    lec = Lecturer("Лектор", "Лекторов")
    dept.assign_head(lec)
    assert dept.head == lec
    assert dept.head_name == lec.full_name
    assert dept.staff_count == 1

    lec2 = Lecturer("Второй", "Второй")
    dept.add_teacher(lec2)
    assert dept.staff_count == 2
    assert lec2.department == dept

    dept.remove_teacher(lec2)
    assert dept.staff_count == 1
    assert lec2.department is None

    with pytest.raises(ValueError):
        dept.remove_teacher(lec2)
