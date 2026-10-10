import pytest
from lab3.domain.fleet.fuel_truck import FuelTruck
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.fleet.private_jet import PrivateJet
from lab3.domain.maintenance.catering_task import CateringTask
from lab3.domain.maintenance.cleaning_task import CleaningTask
from lab3.domain.maintenance.maintenance_inspection import MaintenanceInspection
from lab3.domain.maintenance.refueling_task import RefuelingTask
from lab3.domain.maintenance.weather_report import WeatherReport
from lab3.domain.people.security_officer import SecurityOfficer


def test_weather():
    w_ok = WeatherReport(20.0, 5.0, 5000.0, False)
    assert w_ok.is_safe_for_operations is True

    w_storm = WeatherReport(20.0, 5.0, 5000.0, True)
    assert w_storm.is_safe_for_operations is False

    w_wind = WeatherReport(20.0, 30.0, 5000.0, False)
    assert w_wind.is_safe_for_operations is False

    w_fog = WeatherReport(20.0, 5.0, 200.0, False)
    assert w_fog.is_safe_for_operations is False


def test_service_tasks():
    plane = PassengerAircraft("P", 800.0, "RA-01", 10000.0, 100)
    staff = SecurityOfficer("С", "С", "P", 100.0)

    task = MaintenanceInspection(plane)
    with pytest.raises(ValueError):
        task.execute()

    task.assign_staff(staff)
    assert len(task.assigned_staff) == 1
    res = task.execute()
    assert "успешно завершен" in res
    assert task.status == "Completed"

    truck = FuelTruck("T", 40.0, "A", 5000.0)
    refuel = RefuelingTask(plane, truck, 2000.0)
    refuel.assign_staff(staff)
    refuel.execute()
    assert plane.current_fuel == 2000.0

    clean = CleaningTask(plane, requires_deep_cleaning=True)
    clean.assign_staff(staff)
    assert "Генеральная" in clean.execute()

    jet = PrivateJet("J", 800.0, "RA-J", 5000.0, "VIP")
    cater = CateringTask(jet, meals_count=10, includes_vip=True)
    cater.assign_staff(staff)
    cater.execute()
    assert jet.is_vip_catered is True
