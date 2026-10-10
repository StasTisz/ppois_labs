from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.operations.airline import Airline


def test_airline():
    airline = Airline("Belavia", "B2")
    plane = PassengerAircraft("P", 800.0, "RA-AL", 1000.0, 100)

    assert airline.fleet_size == 0
    airline.register_aircraft(plane)
    assert airline.fleet_size == 1
    assert len(airline.get_fleet()) == 1
