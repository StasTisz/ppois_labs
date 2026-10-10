class DeanOfficeException(Exception):
    """Базовое исключение доменной модели деканата."""


class StudentNotFoundException(DeanOfficeException):
    """Студент не найден в реестре."""


class GroupNotFoundException(DeanOfficeException):
    """Группа не найдена на факультете."""


class DuplicateEnrollmentException(DeanOfficeException):
    """Попытка повторного зачисления."""


class ExpulsionDeniedException(DeanOfficeException):
    """Отказ в отчислении студента."""
