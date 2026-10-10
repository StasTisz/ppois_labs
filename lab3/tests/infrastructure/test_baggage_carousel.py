from datetime import UTC, datetime
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.arrival_flight import ArrivalFlight
from lab3.domain.operations.flight_plan import FlightPlan


def test_baggage_carousel():
    car = BaggageCarousel(2)
    assert car.is_active is False

    plane = PassengerAircraft("P", 800.0, "RA-BC", 1000.0, 100)
    flight = ArrivalFlight("B2-40", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC)))

    car.activate(flight)
    assert car.is_active is True
    assert car.assigned_flight == flight

    car.deactivate()
    assert car.is_active is False
    assert car.assigned_flight is None
