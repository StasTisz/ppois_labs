import pytest

from lab3.domain.people import (
    BaggageHandler,
    CheckInAgent,
    Dispatcher,
    FlightAttendant,
    Passenger,
    Pilot,
    SecurityOfficer,
)


def test_passenger_baggage_and_tickets():
    passenger = Passenger("Ivan", "Ivanov", "AB12345")
    assert passenger.full_name == "Ivan Ivanov"

    passenger.buy_ticket("Ticket_Mock")
    passenger.add_baggage("Baggage_Mock")
    assert passenger.has_tickets
    assert passenger.baggage_count == 1
    assert "Ticket_Mock" in passenger.get_tickets()


def test_pilot_duty_and_hours():
    pilot = Pilot("Alex", "Smith", "US987", 5000.0, "ATPL", is_captain=True)
    with pytest.raises(ValueError):
        pilot.perform_duty()  # Не на смене

    pilot.clock_in()
    result = pilot.perform_duty()
    assert "КВС" in result
    assert pilot.pre_flight_checks_done

    pilot.log_flight_hours(80)
    with pytest.raises(ValueError):
        pilot.log_flight_hours(20)  # Превышение лимита 90


def test_flight_attendant_duty():
    fa = FlightAttendant("Maria", "Ivanova", "RU123", 2000.0, ["En", "Ru"])
    fa.clock_in()
    assert "провел инструктаж" in fa.perform_duty()
    assert fa.safety_briefing_done
    fa.clock_out()
    assert not fa.is_on_shift


def test_dispatcher():
    disp = Dispatcher("John", "Doe", "UK555", 3000.0, 5)
    result = disp.perform_duty()
    assert disp.active_channels == 3
    assert "ведет радиообмен" in result


def test_security_officer():
    sec = SecurityOfficer("Bob", "Guard", "111", 1500.0)
    assert "осуществляет досмотр" in sec.perform_duty()


def test_check_in_agent():
    agent = CheckInAgent("Anna", "Agent", "222", 1800.0, 120)
    agent.perform_duty()
    agent.perform_duty()
    assert agent.passengers_processed == 2


def test_baggage_handler():
    handler = BaggageHandler("Tom", "Lift", "333", 1600.0, True)
    result = handler.perform_duty()
    assert handler.tons_loaded == 0.5
    assert "с помощью погрузчика" in result