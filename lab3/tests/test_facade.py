import pytest
from datetime import datetime
from lab3.domain.facade import AirportFacade
from lab3.domain.exceptions import PassengerNotFoundException, InvalidTicketException, MaintenanceRequiredException
from lab3.domain.fleet import PassengerAircraft, FuelTruck
from lab3.domain.people import Employee, Pilot
from lab3.domain.infrastructure import Runway


def test_facade_e2e_departure():
    facade = AirportFacade("Hub", "HUB")

    # 1. Регистрация инфраструктуры и флота
    runway = Runway("01L", 3000)
    facade.airport.control_tower.add_runway(runway)

    plane = PassengerAircraft("B737", 800.0, "RA-001", 15000.0, 150)
    facade.register_aircraft(plane)

    truck = FuelTruck("ZIL", 60.0, "FT-1", 20000.0)
    facade.register_fuel_truck(truck)

    tech = Pilot("T", "T", "111", 1000.0, "ATPL")
    tech.clock_in()
    facade.register_employee(tech)

    # 2. Создание рейса
    flight = facade.create_departure_flight(
        flight_number="B2-123",
        airline_name="Belavia",
        tail_number="RA-001",
        origin="HUB",
        destination="SVO",
        scheduled_time=datetime.now()
    )
    from lab3.domain.infrastructure import Gate
    flight.assign_gate(Gate("1"))

    # 3. Регистрация пассажира
    passenger = facade.register_passenger("John", "Doe", "AB123")
    ticket = facade.issue_ticket("AB123", "B2-123", "Economy", 200.0)

    # 4. Check-in
    boarding_pass = facade.check_in_passenger("AB123", "B2-123", baggage_weight=15.0)
    assert boarding_pass.seat_number == "1A"
    assert len(flight._manifest) == 1
    assert len(flight._cargo_hold) == 1

    # Проверка исключений при чекине
    with pytest.raises(PassengerNotFoundException):
        facade.check_in_passenger("UNKNOWN", "B2-123")
    with pytest.raises(InvalidTicketException):
        facade.check_in_passenger("AB123", "B2-123")  # Билет уже использован

    # 5. Обслуживание перед вылетом
    plane.requires_maintenance = True  # Имитация посадки до этого
    facade.prepare_flight("B2-123", fuel_amount=5000.0)
    assert plane.current_fuel == 5000.0
    assert not plane.requires_maintenance

    # 6. Взлет
    used_runway = facade.dispatch_takeoff("B2-123")
    assert flight.status == "InFlight"
    assert plane.is_in_flight
    assert not used_runway.is_busy