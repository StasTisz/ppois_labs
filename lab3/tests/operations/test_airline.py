from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.operations.airline import Airline


def test_airline():
    airline = Airline("Belavia", "B2")
    plane = PassengerAircraft("P", 800.0, "RA-AL", 1000.0, 100)

    assert airline.fleet_size == 0
    assert "Belavia" in repr(airline)
    assert airline == Airline("Belavia Belarusian", "B2")
    assert airline != "NotAnAirline"
    assert len({airline, Airline("Belavia2", "B2")}) == 1

    airline.register_aircraft(plane)
    assert airline.fleet_size == 1
    assert len(airline.get_fleet()) == 1

    # Test copy protection
    fleet_copy = airline.fleet
    fleet_copy.clear()
    assert airline.fleet_size == 1

    airline.remove_aircraft(plane)
    assert airline.fleet_size == 0
