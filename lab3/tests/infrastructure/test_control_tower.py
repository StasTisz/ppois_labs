import pytest
from lab3.domain.exceptions import RunwayBusyException, WeatherWarningException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.control_tower import ControlTower
from lab3.domain.infrastructure.runway import Runway


def test_control_tower():
    tower = ControlTower()
    r1 = Runway("28L", 3000)
    plane1 = PassengerAircraft("P1", 800.0, "RA-T1", 1000.0, 100)
    plane2 = PassengerAircraft("P2", 800.0, "RA-T2", 1000.0, 100)

    tower.add_runway(r1)
    runway = tower.request_takeoff(plane1)
    assert runway == r1

    with pytest.raises(RunwayBusyException):
        tower.request_takeoff(plane2)

    r1.clear()
    land_runway = tower.request_landing(plane1)
    assert land_runway == r1

    with pytest.raises(RunwayBusyException):
        tower.request_landing(plane2)

    r1.clear()
    tower.update_weather(is_safe=False)
    with pytest.raises(WeatherWarningException):
        tower.request_takeoff(plane1)
    with pytest.raises(WeatherWarningException):
        tower.request_landing(plane1)
