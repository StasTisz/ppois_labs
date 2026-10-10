import pytest
from lab3.domain.exceptions import (
    BaggageOverweightException,
    FlightDelayedException,
    InvalidTicketException,
)
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.arrival_flight import ArrivalFlight
from lab3.domain.operations.baggage import Baggage
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.operations.schedule import Schedule
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger
from datetime import UTC, datetime


def test_baggage_and_ticket():
    p = Passenger("П", "П", "P-1")
    bag = Baggage(20.0, p)
    assert bag.owner == p
    bag.check_weight()

    heavy = Baggage(30.0, p)
    with pytest.raises(BaggageOverweightException):
        heavy.check_weight()

    ticket = Ticket(p, "B2-100", "Economy", 150.0)
    assert ticket.is_used is False
    ticket.use_ticket()
    assert ticket.is_used is True
    with pytest.raises(InvalidTicketException):
        ticket.use_ticket()


def test_flight_lifecycle():
    plane = PassengerAircraft("P", 800.0, "RA-FL", 10000.0, 100)
    airline = Airline("Belavia", "B2")
    airline.register_aircraft(plane)
    assert airline.fleet_size == 1

    plan = FlightPlan("MSQ", "LED", datetime.now(UTC))
    flight = DepartureFlight("B2-200", airline, plane, plan)
    gate = Gate("G1")
    flight.assign_gate(gate)
    assert flight.assigned_gate == gate

    p = Passenger("Пасс", "Пассов", "P-99")
    t = Ticket(p, "B2-200", "Economy", 200.0)
    bp = flight.check_in_passenger(p, t)
    assert bp.ticket == t
    assert bp.gate == gate
    assert len(flight.manifest) == 1

    b = Baggage(15.0, p)
    flight.load_baggage(b)
    assert len(flight.cargo_hold) == 1

    flight.start_boarding()
    assert flight.status == "Boarding"
    assert gate.is_open is True

    flight.cancel()
    assert flight.status == "Cancelled"

    with pytest.raises(FlightDelayedException):
        flight.check_in_passenger(p, t)

    arr = ArrivalFlight("B2-201", airline, plane, plan)
    car = BaggageCarousel(2)
    arr.assign_carousel(car)
    arr.land()
    assert arr.status == "Landed"
    assert car.is_active is True

    sched = Schedule()
    sched.add_flight(flight)
    sched.add_flight(arr)
    assert len(sched.get_departures()) == 1
    assert len(sched.get_arrivals()) == 1
