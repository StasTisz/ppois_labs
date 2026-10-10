import pytest
from lab3.domain.people.baggage_handler import BaggageHandler
from lab3.domain.people.check_in_agent import CheckInAgent
from lab3.domain.people.dispatcher import Dispatcher
from lab3.domain.people.flight_attendant import FlightAttendant
from lab3.domain.people.passenger import Passenger
from lab3.domain.people.pilot import Pilot
from lab3.domain.people.security_officer import SecurityOfficer


def test_passenger():
    p = Passenger("Иван", "Иванов", "111")
    assert p.full_name == "Иван Иванов"
    assert p.has_tickets is False
    assert p.baggage_count == 0


def test_staff():
    pilot = Pilot("Капитан", "К", "222", 3000.0, "ATPL", is_captain=True)
    with pytest.raises(ValueError):
        pilot.perform_duty()
    pilot.clock_in()
    assert "КВС" in pilot.perform_duty()
    pilot.log_flight_hours(10)
    assert pilot.flight_hours == 10
    with pytest.raises(ValueError):
        pilot.log_flight_hours(100)

    fa = FlightAttendant("Стюардесса", "С", "333", 1000.0, ["RU", "EN"])
    fa.clock_in()
    assert "инструктаж" in fa.perform_duty()

    disp = Dispatcher("Диспетчер", "Д", "444", 2000.0, 1)
    assert "радиообмен" in disp.perform_duty()

    so = SecurityOfficer("Офицер", "О", "555", 1500.0)
    assert "досмотр" in so.perform_duty()

    agent = CheckInAgent("Агент", "А", "666", 800.0, 200)
    assert agent.passengers_processed == 0
    agent.perform_duty()
    assert agent.passengers_processed == 1

    handler = BaggageHandler("Грузчик", "Г", "777", 700.0, heavy_machinery_license=True)
    assert handler.tons_loaded == 0.0
    handler.perform_duty()
    assert handler.tons_loaded == 0.5
