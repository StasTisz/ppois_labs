class DeanOfficeException(Exception):
    """Базовое исключение доменной модели деканата."""


class StudentNotFoundException(DeanOfficeException):
    """Студент или зачетная книжка не найдены в реестре."""


class GroupNotFoundException(DeanOfficeException):
    """Учебная группа не найдена на факультете."""


class DuplicateEnrollmentException(DeanOfficeException):
    """Попытка повторного зачисления студента в группу."""


class ExpulsionDeniedException(DeanOfficeException):
    """Отказ в отчислении при отсутствии законных оснований."""


class InsufficientFundsException(DeanOfficeException):
    """Недостаточно средств на банковском счете."""


class AccountBlockedException(DeanOfficeException):
    """Попытка операции по заблокированному банковскому счету."""


class InvalidScoreException(DeanOfficeException):
    """Оценка выходит за допустимый диапазон (0-10)."""


class RoomCapacityExceededException(DeanOfficeException):
    """Превышение лимита мест в комнате общежития."""


class ResidentNotFoundException(DeanOfficeException):
    """Студент не проживает в указанной комнате."""


class BookNotAvailableException(DeanOfficeException):
    """Отсутствие доступных экземпляров книги в библиотеке."""


class LibraryLimitExceededException(DeanOfficeException):
    """Превышение лимита одновременно взятых книг."""


class ScheduleCollisionException(DeanOfficeException):
    """Накладка по аудитории, преподавателю или группе в расписании."""


class DocumentNotSignedException(DeanOfficeException):
    """Попытка исполнения неподписанного приказа."""
