import pytest
from datetime import datetime, timedelta
from lab3.domain.exceptions import SecurityCheckFailedException, VisaExpiredException
from lab3.domain.security import Visa, CustomsDeclaration, MetalDetector, XRayScanner, SecurityCheckpoint, \
    PassportControl, CustomsControl
from lab3.domain.maintenance import WeatherReport, MaintenanceInspection, RefuelingTask, CleaningTask, CateringTask
from lab3.domain.fleet import PassengerAircraft, PrivateJet, FuelTruck
from lab3.domain.people import SecurityOfficer, Pilot


def test_visa_validity():
    valid_date = datetime.now() + timedelta(days=10)
    expired_date = datetime.now() - timedelta(days=10)
    assert Visa("UK", valid_date).is_valid(datetime.now())
    assert not Visa("UK", expired_date).is_valid(datetime.now())


def test_customs_declaration():
    decl = CustomsDeclaration("P1", ["Laptop"], 5000.0)
    assert not decl.is_approved
    decl.approve()
    assert decl.is_approved


def test_security_checkpoint():
    checkpoint = SecurityCheckpoint(1)
    checkpoint.assign_equipment(MetalDetector("MD1"), XRayScanner("XR1"))

    officer = SecurityOfficer("O", "O", "1", 1000)
    officer.clock_in()
    checkpoint.assign_officer(officer)

    # Мок-пассажир для прохождения (сканеры возвращают True)
    class MockPassenger:
        full_name = "Mock"

    checkpoint.process_passenger(MockPassenger(), None)


def test_passport_control():
    control = PassportControl(1)

    class MockPassenger:
        full_name = "Mock"

    valid_visa = Visa("USA", datetime.now() + timedelta(days=10))
    expired_visa = Visa("USA", datetime.now() - timedelta(days=10))
    wrong_visa = Visa("UK", datetime.now() + timedelta(days=10))

    control.check_documents(MockPassenger(), valid_visa, "USA")

    with pytest.raises(VisaExpiredException):
        control.check_documents(MockPassenger(), None, "USA")
    with pytest.raises(VisaExpiredException):
        control.check_documents(MockPassenger(), expired_visa, "USA")
    with pytest.raises(VisaExpiredException):
        control.check_documents(MockPassenger(), wrong_visa, "USA")


def test_customs_control():
    control = CustomsControl()
    valid_decl = CustomsDeclaration("P1", [], 5000.0)
    invalid_decl = CustomsDeclaration("P2", [], 15000.0)

    control.inspect_declaration(valid_decl)
    with pytest.raises(SecurityCheckFailedException):
        control.inspect_declaration(invalid_decl)


def test_weather_report():
    safe_weather = WeatherReport(20.0, 5.0, 5000.0, False)
    stormy = WeatherReport(20.0, 5.0, 5000.0, True)
    windy = WeatherReport(20.0, 30.0, 5000.0, False)
    foggy = WeatherReport(20.0, 5.0, 200.0, False)

    assert safe_weather.is_safe_for_operations
    assert not stormy.is_safe_for_operations
    assert not windy.is_safe_for_operations
    assert not foggy.is_safe_for_operations


def test_service_tasks():
    plane = PassengerAircraft("B737", 850.0, "RA-111", 15000.0, 150)
    truck = FuelTruck("T", 50.0, "1", 10000.0)
    emp = Pilot("P", "P", "1", 1000.0, "CPL")

    # Maintenance
    insp = MaintenanceInspection(plane)
    with pytest.raises(ValueError):
        insp.execute()  # Без персонала
    insp.assign_staff(emp)
    assert "успешно завершен" in insp.execute()
    assert plane.oxygen_masks_tested

    # Refuel
    refuel = RefuelingTask(plane, truck, 5000.0)
    refuel.assign_staff(emp)
    refuel.execute()
    assert plane.current_fuel == 5000.0

    # Cleaning
    clean = CleaningTask(plane, True)
    clean.assign_staff(emp)
    assert "Генеральная" in clean.execute()

    # Catering (VIP)
    vip_jet = PrivateJet("Jet", 900.0, "V1", 10000.0, "Owner")
    cat = CateringTask(vip_jet, 5, includes_vip=True)
    cat.assign_staff(emp)
    cat.execute()
    assert vip_jet.is_vip_catered