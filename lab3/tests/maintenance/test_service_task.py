import pytest
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.maintenance.service_task import ServiceTask
from lab3.domain.people.security_officer import SecurityOfficer


class DummyTask(ServiceTask):
    def execute(self) -> str:
        self._start()
        self._complete()
        return "Done"


def test_service_task():
    plane = PassengerAircraft("P", 800.0, "RA-S", 1000.0, 100)
    task = DummyTask(plane)
    assert task.status == "Pending"

    with pytest.raises(ValueError):
        task.execute()

    staff = SecurityOfficer("С", "С", "P", 100.0)
    task.assign_staff(staff)
    assert len(task.assigned_staff) == 1
    assert task.execute() == "Done"
    assert task.status == "Completed"
