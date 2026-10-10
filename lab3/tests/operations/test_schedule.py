from datetime import UTC, datetime
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.arrival_flight import ArrivalFlight
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.operations.schedule import Schedule


def test_schedule():
    sched = Schedule()
    plane = PassengerAircraft("P", 800.0, "RA-SC", 1000.0, 100)
    airline = Airline("A", "A")
    plan = FlightPlan("O", "D", datetime.now(UTC))

    dep = DepartureFlight("D-1", airline, plane, plan)
    arr = ArrivalFlight("A-1", airline, plane, plan)

    sched.add_flight(dep)
    sched.add_flight(arr)
    assert len(sched.get_departures()) == 1
    assert len(sched.get_arrivals()) == 1
