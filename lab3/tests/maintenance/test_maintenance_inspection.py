from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.maintenance.maintenance_inspection import MaintenanceInspection
from lab3.domain.people.security_officer import SecurityOfficer


def test_maintenance_inspection():
    plane = PassengerAircraft("P", 800.0, "RA-MI", 1000.0, 100)
    plane.requires_maintenance = True
    inspection = MaintenanceInspection(plane)

    staff = SecurityOfficer("Иван", "И", "P-9", 1000.0)
    inspection.assign_staff(staff)
    msg = inspection.execute()

    assert "RA-MI" in msg
    assert plane.requires_maintenance is False
