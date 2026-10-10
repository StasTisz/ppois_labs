from datetime import datetime

import pytest

from lab3.domain.exceptions import (
    BaggageOverweightException,
    FlightDelayedException,
    InvalidTicketException,
)
from lab3.domain.fleet import PassengerAircraft
from lab3.domain.infrastructure import BaggageCarousel, Gate
from lab3.domain.operations import (
    Airline,
    ArrivalFlight,
    Baggage,
    DepartureFlight,
    FlightPlan,
    Schedule,
    Ticket,
)
from lab3.domain.people import Passenger


def test_baggage_weight():
    valid_baggage = Baggage(20.0, "Pass1")
    valid_baggage.check_weight()  # Не должно падать

    heavy_baggage = Baggage(25.0, "Pass2")
    with pytest.raises(BaggageOverweightException):
        heavy_baggage.check_weight()


def test_ticket_usage():
    ticket = Ticket("Pass_ID", "B2-100", "Economy", 150.0)
    ticket.use_ticket()
    assert ticket.is_used
    with pytest.raises(InvalidTicketException):
        ticket.use_ticket()


def test_airline_registration():
    belavia = Airline("Belavia", "B2")
    plane = PassengerAircraft("E195", 800.0, "EW-111", 12000.0, 110)
    belavia.register_aircraft(plane)
    assert belavia.fleet_size == 1


def test_departure_flight_check_in():
    airline = Airline("Belavia", "B2")
    plane = PassengerAircraft("E195", 800.0, "EW-111", 12000.0, 110)
    plan = FlightPlan("MSQ", "SVO", datetime.now())
    flight = DepartureFlight("B2-100", airline, plane, plan)

    passenger = Passenger("I", "I", "123")
    ticket = Ticket(passenger.person_id, "B2-100", "Economy", 100.0)

    gate = Gate("1")
    flight.assign_gate(gate)

    boarding_pass = flight.check_in_passenger(passenger, ticket)
    assert boarding_pass.seat_number == "1A"
    assert boarding_pass.gate_number == "1"

    ticket2 = Ticket(passenger.person_id, "B2-100", "Economy", 100.0)
    boarding_pass2 = flight.check_in_passenger(passenger, ticket2)
    assert boarding_pass2.seat_number == "1B"

    baggage = Baggage(15.0, passenger.person_id)
    flight.load_baggage(baggage)
    assert len(flight._cargo_hold) == 1


def test_departure_flight_exceptions():
    airline = Airline("Belavia", "B2")
    plane = PassengerAircraft("E195", 800.0, "EW-111", 12000.0, 110)
    plan = FlightPlan("MSQ", "SVO", datetime.now())
    flight = DepartureFlight("B2-100", airline, plane, plan)

    passenger = Passenger("I", "I", "123")
    wrong_ticket = Ticket(passenger.person_id, "SU-200", "Economy", 100.0)

    with pytest.raises(InvalidTicketException):
        flight.check_in_passenger(passenger, wrong_ticket)

    flight.delay("Snow")
    valid_ticket = Ticket(passenger.person_id, "B2-100", "Economy", 100.0)
    with pytest.raises(FlightDelayedException):
        flight.check_in_passenger(passenger, valid_ticket)


def test_arrival_flight_and_schedule():
    airline = Airline("Belavia", "B2")
    plane = PassengerAircraft("E195", 800.0, "EW-111", 12000.0, 110)
    plan = FlightPlan("SVO", "MSQ", datetime.now())
    flight = ArrivalFlight("B2-200", airline, plane, plan)

    carousel = BaggageCarousel(1)
    flight.assign_carousel(carousel)
    flight.land()
    assert flight.status == "Landed"
    assert carousel.is_active

    schedule = Schedule()
    schedule.add_flight(flight)
    assert len(schedule.get_arrivals()) == 1
    assert len(schedule.get_departures()) == 0