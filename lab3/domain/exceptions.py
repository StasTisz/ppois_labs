class AirportException(Exception):
    """Базовое исключение доменной модели аэропорта."""

class FlightDelayedException(AirportException):
    """Выбрасывается при попытке выполнить штатные операции с отложенным рейсом."""

class BoardingClosedException(AirportException):
    """Выбрасывается при попытке посадки пассажира после закрытия гейта."""

class InvalidTicketException(AirportException):
    """Выбрасывается при несовпадении данных билета и пассажира или отсутствии брони."""

class BaggageOverweightException(AirportException):
    """Выбрасывается при превышении допустимого веса багажа."""

class RunwayBusyException(AirportException):
    """Выбрасывается при попытке посадки или взлета на занятую взлетно-посадочную полосу."""

class SecurityCheckFailedException(AirportException):
    """Выбрасывается, если пассажир или багаж не прошли досмотр службы безопасности."""

class VisaExpiredException(AirportException):
    """Выбрасывается на пограничном контроле при отсутствии или просрочке визы."""

class GateNotAssignedException(AirportException):
    """Выбрасывается при попытке начать посадку без привязки рейса к конкретному гейту."""

class MaintenanceRequiredException(AirportException):
    """Выбрасывается при попытке отправить в рейс борт, не прошедший технический осмотр."""

class NoAvailableCrewException(AirportException):
    """Выбрасывается при нехватке пилотов или бортпроводников для формирования экипажа."""

class WeatherWarningException(AirportException):
    """Выбрасывается диспетчерской вышкой при запрете вылетов из-за плохих метеоусловий."""

class CapacityExceededException(AirportException):
    """Выбрасывается при попытке продать билет на полностью заполненный рейс или переполнить зал ожидания."""

class PassengerNotFoundException(AirportException):
    """Выбрасывается при поиске несуществующего пассажира в манифесте рейса."""
