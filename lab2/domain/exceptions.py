class DeanOfficeException(Exception):
    """Базовое исключение доменной модели деканата."""
    pass

class StudentNotFoundException(DeanOfficeException): pass
class GroupNotFoundException(DeanOfficeException): pass
class DuplicateEnrollmentException(DeanOfficeException): pass
class ExpulsionDeniedException(DeanOfficeException): pass
class InsufficientFundsException(DeanOfficeException): pass
class AccountBlockedException(DeanOfficeException): pass
class InvalidScoreException(DeanOfficeException): pass
class RoomCapacityExceededException(DeanOfficeException): pass
class ResidentNotFoundException(DeanOfficeException): pass
class BookNotAvailableException(DeanOfficeException): pass
class LibraryLimitExceededException(DeanOfficeException): pass
class ScheduleCollisionException(DeanOfficeException): pass
class DocumentNotSignedException(DeanOfficeException): pass