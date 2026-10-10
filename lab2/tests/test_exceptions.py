import pytest
from lab2.domain.exceptions import (
    AccountBlockedException,
    BookNotAvailableException,
    DeanOfficeException,
    DocumentNotSignedException,
    DuplicateEnrollmentException,
    ExpulsionDeniedException,
    GroupNotFoundException,
    InsufficientFundsException,
    InvalidScoreException,
    LibraryLimitExceededException,
    ResidentNotFoundException,
    RoomCapacityExceededException,
    ScheduleCollisionException,
    StudentNotFoundException,
)


def test_exceptions_hierarchy():
    exceptions = [
        StudentNotFoundException,
        GroupNotFoundException,
        DuplicateEnrollmentException,
        ExpulsionDeniedException,
        InsufficientFundsException,
        AccountBlockedException,
        InvalidScoreException,
        RoomCapacityExceededException,
        ResidentNotFoundException,
        BookNotAvailableException,
        LibraryLimitExceededException,
        ScheduleCollisionException,
        DocumentNotSignedException,
    ]
    for exc in exceptions:
        assert issubclass(exc, DeanOfficeException)
        with pytest.raises(exc):
            raise exc("Test exception message")
