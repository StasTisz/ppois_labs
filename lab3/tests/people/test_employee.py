from lab3.domain.people.employee import Employee


class DummyEmployee(Employee):
    def perform_duty(self) -> str:
        return "Работает"


def test_employee():
    emp = DummyEmployee("Сергей", "С", "P-123", salary=1200.0)
    assert emp.salary == 1200.0
    assert emp.is_on_shift is False

    emp.clock_in()
    assert emp.is_on_shift is True
    assert emp.perform_duty() == "Работает"

    emp.clock_out()
    assert emp.is_on_shift is False
