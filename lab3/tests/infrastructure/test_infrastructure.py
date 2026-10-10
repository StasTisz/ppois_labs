import pytest
from lab3.domain.exceptions import (
    CapacityExceededException,
    GateNotAssignedException,
    RunwayBusyException,
    WeatherWarningException,
)
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.airport import Airport
from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.infrastructure.check_in_counter import CheckInCounter
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.infrastructure.hangar import Hangar
from lab3.domain.infrastructure.lounge import Lounge
from lab3.domain.infrastructure.parking_lot import ParkingLot
from lab3.domain.infrastructure.runway import Runway
from lab3.domain.infrastructure.terminal import Terminal
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.baggage import Baggage
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.people.check_in_agent import CheckInAgent
from lab3.domain.people.passenger import Passenger
from datetime import UTC, datetime


def test_runway_and_tower():
    plane1 = PassengerAircraft("P1", 800.0, "RA-01", 1000.0, 100)
    plane2 = PassengerAircraft("P2", 800.0, "RA-02", 1000.0, 100)
    runway = Runway("09L", 3000)

    runway.occupy(plane1)
    with pytest.raises(RunwayBusyException):
        runway.occupy(plane2)
    runway.clear()
    assert runway.is_busy is False

    airport = Airport("Minsk-2", "MSQ")
    tower = airport.control_tower
    tower.add_runway(runway)
    assert tower.request_takeoff(plane1) == runway
    with pytest.raises(RunwayBusyException):
        tower.request_takeoff(plane2)
    runway.clear()

    tower.update_weather(is_safe=False)
    with pytest.raises(WeatherWarningException):
        tower.request_takeoff(plane1)
    with pytest.raises(WeatherWarningException):
        tower.request_landing(plane1)


def test_terminal_components():
    p = Passenger("Иван", "Иванов", "AB123456")
    lounge = Lounge("VIP", capacity=1, is_vip=True)
    lounge.enter(p)
    assert lounge.current_occupancy == 1
    with pytest.raises(CapacityExceededException):
        lounge.enter(Passenger("П", "П", "CD987654"))
    lounge.exit(p)
    assert lounge.current_occupancy == 0

    hangar = Hangar("H1", capacity=1)
    plane = PassengerAircraft("P", 800.0, "RA-H", 1000.0, 50)
    hangar.store_aircraft(plane)
    with pytest.raises(CapacityExceededException):
        hangar.store_aircraft(plane)
    hangar.release_aircraft(plane)

    lot = ParkingLot("P1", capacity=1)
    lot.park_car("1111-AA")
    with pytest.raises(CapacityExceededException):
        lot.park_car("2222-BB")
    lot.remove_car("1111-AA")

    gate = Gate("A1")
    with pytest.raises(GateNotAssignedException):
        gate.open_gate()

    terminal = Terminal("T1")
    terminal.add_gate(gate)
    assert terminal.get_gate("A1") == gate
    assert terminal.get_gate("B2") is None

    agent = CheckInAgent("А", "А", "P1", 100.0, 120)
    plan = FlightPlan("MSQ", "DME", datetime.now(UTC))
    flight = DepartureFlight("B2-100", Airline("Belavia", "B2"), plane, plan)
    counter = CheckInCounter(1)
    with pytest.raises(ValueError):
        counter.accept_baggage(Baggage(10.0, p))
    counter.open_counter(agent, flight)
    counter.accept_baggage(Baggage(10.0, p))
    counter.close_counter()

    car = BaggageCarousel(1)
    car.activate(flight)
    assert car.is_active is True
    car.deactivate()
    assert car.is_active is False
