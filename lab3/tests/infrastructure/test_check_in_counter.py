from datetime import UTC, datetime
import pytest
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.check_in_counter import CheckInCounter
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.baggage import Baggage
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.people.check_in_agent import CheckInAgent
from lab3.domain.people.passenger import Passenger


def test_check_in_counter():
    counter = CheckInCounter(3)
    agent = CheckInAgent("Анна", "А", "P-10", 900.0, 180)
    plane = PassengerAircraft("P", 800.0, "RA-C", 1000.0, 100)
    flight = DepartureFlight("B2-30", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC)))
    passenger = Passenger("П", "П", "P-01")

    with pytest.raises(ValueError):
        counter.accept_baggage(Baggage(12.0, passenger))

    counter.open_counter(agent, flight)
    assert counter.is_open is True
    assert counter.current_agent == agent
    assert counter.assigned_flight == flight

    bag = Baggage(15.0, passenger)
    counter.accept_baggage(bag)
    assert len(counter._accepted_baggage) == 1

    counter.close_counter()
    assert counter.is_open is False
    assert counter.current_agent is None
