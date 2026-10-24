from lab3.domain.fleet.fuel_truck import FuelTruck
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.maintenance.refueling_task import RefuelingTask
from lab3.domain.people.security_officer import SecurityOfficer


def test_refueling_task():
    plane = PassengerAircraft("P", 800.0, "RA-RF", 10000.0, 100)
    truck = FuelTruck("T", 40.0, "FT-01", 8000.0)
    task = RefuelingTask(plane, truck, 3000.0)

    staff = SecurityOfficer("С", "С", "P", 100.0)
    task.assign_staff(staff)
    msg = task.execute()

    assert plane.current_fuel == 3000.0
    assert "заправлен на 3000.0 л" in msg
