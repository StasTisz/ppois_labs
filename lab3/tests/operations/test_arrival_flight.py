from datetime import UTC, datetime
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.arrival_flight import ArrivalFlight
from lab3.domain.operations.flight_plan import FlightPlan


def test_arrival_flight():
    plane = PassengerAircraft("P", 800.0, "RA-AF", 1000.0, 100)
    flight = ArrivalFlight("B2-20", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC)))
    car = BaggageCarousel(5)

    flight.assign_carousel(car)
    flight.land()
    assert flight.status == "Landed"
    assert car.is_active is True
