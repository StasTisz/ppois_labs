import pytest
from datetime import UTC, datetime
from lab3.domain.exceptions import (
    InvalidTicketException,
    MaintenanceRequiredException,
    PassengerNotFoundException,
)
from lab3.domain.facade.airport_facade import AirportFacade
from lab3.domain.fleet.fuel_truck import FuelTruck
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.runway import Runway
from lab3.domain.people.employee import Employee


class DummyTech(Employee):
    def perform_duty(self) -> str:
        return "Работает"


def test_facade_end_to_end():
    facade = AirportFacade("Minsk International", "MSQ")
    plane = PassengerAircraft("B737", 850.0, "EW-001PA", 20000.0, 160)
    truck = FuelTruck("FT-500", 50.0, "T001TT", 10000.0)

    facade.register_aircraft(plane)
    facade.register_fuel_truck(truck)
    assert len(facade.aircrafts) == 1
    assert len(facade.fuel_trucks) == 1

    tech = DummyTech("Мастер", "М", "T-01", 1000.0)
    tech.clock_in()
    facade.register_employee(tech)
    assert len(facade.employees) == 1

    p = facade.register_passenger("Иван", "Иванов", "MP1234567")
    assert len(facade.passengers) == 1

    flight = facade.create_departure_flight(
        "B2-973", "Belavia", "EW-001PA", "MSQ", "SVO", datetime.now(UTC)
    )

    ticket = facade.issue_ticket("MP1234567", "B2-973", "Economy", 120.0)
    assert ticket.passenger == p
    assert len(facade.tickets) == 1

    with pytest.raises(PassengerNotFoundException):
        facade.issue_ticket("UNKNOWN", "B2-973", "Economy", 120.0)

    with pytest.raises(ValueError):
        facade.create_departure_flight("B2-999", "B2", "UNKNOWN", "A", "B", datetime.now(UTC))

    bp = facade.check_in_passenger("MP1234567", "B2-973", baggage_weight=18.0)
    assert bp.ticket == ticket

    with pytest.raises(InvalidTicketException):
        facade.check_in_passenger("MP1234567", "B2-973")

    facade.prepare_flight("B2-973", fuel_amount=4000.0)
    assert plane.current_fuel == 4000.0

    runway = Runway("31R", 3600)
    facade.airport.control_tower.add_runway(runway)

    plane.requires_maintenance = True
    with pytest.raises(MaintenanceRequiredException):
        facade.dispatch_takeoff("B2-973")

    plane.requires_maintenance = False
    used_runway = facade.dispatch_takeoff("B2-973")
    assert used_runway == runway
    assert flight.status == "InFlight"
