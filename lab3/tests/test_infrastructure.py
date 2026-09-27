import pytest
from lab3.domain.exceptions import RunwayBusyException, GateNotAssignedException, CapacityExceededException, \
    WeatherWarningException
from lab3.domain.infrastructure import Runway, Gate, CheckInCounter, BaggageCarousel, Lounge, Terminal, ControlTower, \
    Hangar, ParkingLot, Airport


def test_runway_occupy_and_clear():
    runway = Runway("27R", 3000)
    assert not runway.is_busy
    runway.occupy("Aircraft_Mock")
    assert runway.is_busy
    assert runway.current_aircraft == "Aircraft_Mock"

    with pytest.raises(RunwayBusyException):
        runway.occupy("Another_Aircraft")

    runway.clear()
    assert not runway.is_busy
    assert runway.current_aircraft is None


def test_gate_assign_and_open():
    gate = Gate("A12")
    gate.assign_flight("Flight_Mock")
    assert gate.current_flight == "Flight_Mock"

    with pytest.raises(ValueError):
        gate.assign_flight("Another_Flight")

    gate.open_gate()
    assert gate.is_open
    gate.clear_gate()
    assert not gate.is_open
    assert gate.current_flight is None


def test_gate_open_without_flight():
    gate = Gate("B1")
    with pytest.raises(GateNotAssignedException):
        gate.open_gate()


def test_check_in_counter():
    counter = CheckInCounter(1)
    counter.open_counter("Agent_Mock", "Flight_Mock")
    assert counter.is_open
    counter.accept_baggage("Baggage_1")
    assert len(counter._accepted_baggage) == 1

    counter.close_counter()
    assert not counter.is_open
    assert len(counter._accepted_baggage) == 0

    with pytest.raises(ValueError):
        counter.accept_baggage("Baggage_2")


def test_baggage_carousel():
    carousel = BaggageCarousel(5)
    assert not carousel.is_active
    carousel.activate("Flight_Mock")
    assert carousel.is_active
    carousel.deactivate()
    assert not carousel.is_active


def test_lounge_capacity():
    lounge = Lounge("Business", capacity=2)
    lounge.enter("Pass_1")
    lounge.enter("Pass_2")
    assert lounge.current_occupancy == 2

    with pytest.raises(CapacityExceededException):
        lounge.enter("Pass_3")

    lounge.exit("Pass_1")
    assert lounge.current_occupancy == 1


def test_terminal_aggregation():
    terminal = Terminal("T1")
    gate = Gate("A1")
    terminal.add_gate(gate)
    assert terminal.get_gate("A1") == gate
    assert terminal.get_gate("B1") is None


def test_control_tower_weather_and_takeoff():
    tower = ControlTower()
    runway = Runway("09L", 2500)
    tower.add_runway(runway)

    tower.update_weather(False)
    with pytest.raises(WeatherWarningException):
        tower.request_takeoff("Aircraft")

    tower.update_weather(True)
    assigned_runway = tower.request_takeoff("Aircraft_1")
    assert assigned_runway.number == "09L"
    assert assigned_runway.is_busy

    with pytest.raises(RunwayBusyException):
        tower.request_landing("Aircraft_2")


def test_hangar_storage():
    hangar = Hangar("H1", 1)
    hangar.store_aircraft("Plane_1")
    with pytest.raises(CapacityExceededException):
        hangar.store_aircraft("Plane_2")
    hangar.release_aircraft("Plane_1")
    assert len(hangar._aircrafts) == 0


def test_parking_lot():
    lot = ParkingLot("P1", 2)
    lot.park_car("ABC-123")
    lot.park_car("XYZ-789")
    with pytest.raises(CapacityExceededException):
        lot.park_car("QWE-456")
    lot.remove_car("ABC-123")
    lot.park_car("QWE-456")
    assert len(lot._parked_cars) == 2


def test_airport_facade_struct():
    airport = Airport("Minsk National", "MSQ")
    airport.add_terminal(Terminal("T1"))
    assert airport.get_terminal("T1") is not None