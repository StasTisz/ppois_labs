import pytest
from lab2.domain.people.employee import Employee


def test_employee():
    emp = Employee("Сотрудник", "Сотрудников")
    assert emp.salary == 0.0
    emp.promote("Директор", salary_increase=100.0)
    assert emp.position == "Директор"
    assert emp.salary == 100.0

    emp.change_salary(250.0)
    assert emp.salary == 250.0

    with pytest.raises(ValueError):
        emp.change_salary(-10)
