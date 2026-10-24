from lab3.domain.fleet.follow_me_car import FollowMeCar
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft


def test_follow_me_car():
    car = FollowMeCar("Skoda-FMC", 80.0, "FM-07")
    plane = PassengerAircraft("B737", 850.0, "EW-404PA", 15000.0, 170)

    msg = car.lead_aircraft(plane, "Stand 24")
    assert "EW-404PA" in msg
    assert "Stand 24" in msg
    assert car.is_available is True

    car.perform_maintenance()
    assert car.lightbar_tested is True
