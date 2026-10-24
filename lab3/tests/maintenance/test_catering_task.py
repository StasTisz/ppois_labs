from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.fleet.private_jet import PrivateJet
from lab3.domain.maintenance.catering_task import CateringTask
from lab3.domain.people.security_officer import SecurityOfficer


def test_catering_task():
    plane = PassengerAircraft("P", 800.0, "RA-CT", 1000.0, 100)
    jet = PrivateJet("J", 800.0, "RA-VJ", 1000.0, "VIP Owner")
    staff = SecurityOfficer("С", "С", "P", 100.0)

    task1 = CateringTask(plane, meals_count=120)
    task1.assign_staff(staff)
    assert "120 порций" in task1.execute()

    task2 = CateringTask(jet, meals_count=10, includes_vip=True)
    task2.assign_staff(staff)
    task2.execute()
    assert jet.is_vip_catered is True
