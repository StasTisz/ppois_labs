from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.maintenance.cleaning_task import CleaningTask
from lab3.domain.people.security_officer import SecurityOfficer


def test_cleaning_task():
    plane = PassengerAircraft("P", 800.0, "RA-CL", 1000.0, 100)
    staff = SecurityOfficer("С", "С", "P", 100.0)

    standard = CleaningTask(plane, requires_deep_cleaning=False)
    standard.assign_staff(staff)
    assert "Стандартная" in standard.execute()

    deep = CleaningTask(plane, requires_deep_cleaning=True)
    deep.assign_staff(staff)
    assert "Генеральная" in deep.execute()
