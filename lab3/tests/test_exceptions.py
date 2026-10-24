import pytest

from lab3.domain.exceptions import (
    AirportException,
    BaggageOverweightException,
    BoardingClosedException,
    CapacityExceededException,
    FlightDelayedException,
    GateNotAssignedException,
    InvalidTicketException,
    MaintenanceRequiredException,
    NoAvailableCrewException,
    PassengerNotFoundException,
    RunwayBusyException,
    SecurityCheckFailedException,
    VisaExpiredException,
    WeatherWarningException,
)


def test_exceptions_hierarchy():
    exceptions = [
        FlightDelayedException,
        BoardingClosedException,
        InvalidTicketException,
        BaggageOverweightException,
        RunwayBusyException,
        SecurityCheckFailedException,
        VisaExpiredException,
        GateNotAssignedException,
        MaintenanceRequiredException,
        NoAvailableCrewException,
        WeatherWarningException,
        CapacityExceededException,
        PassengerNotFoundException,
    ]
    for exc in exceptions:
        assert issubclass(exc, AirportException)
        with pytest.raises(exc):
            raise exc("Test exception message")
