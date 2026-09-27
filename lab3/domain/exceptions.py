class AirportException(Exception):
    """Базовое исключение доменной модели аэропорта."""
    pass

class FlightDelayedException(AirportException):
    """Выбрасывается при попытке выполнить штатные операции с отложенным рейсом."""
    pass

class BoardingClosedException(AirportException):
    """Выбрасывается при попытке посадки пассажира после закрытия гейта."""
    pass

class InvalidTicketException(AirportException):
    """Выбрасывается при несовпадении данных билета и пассажира или отсутствии брони."""
    pass

class BaggageOverweightException(AirportException):
    """Выбрасывается при превышении допустимого веса багажа."""
    pass

class RunwayBusyException(AirportException):
    """Выбрасывается при попытке посадки или взлета на занятую взлетно-посадочную полосу."""
    pass

class SecurityCheckFailedException(AirportException):
    """Выбрасывается, если пассажир или багаж не прошли досмотр службы безопасности."""
    pass

class VisaExpiredException(AirportException):
    """Выбрасывается на пограничном контроле при отсутствии или просрочке визы."""
    pass

class GateNotAssignedException(AirportException):
    """Выбрасывается при попытке начать посадку без привязки рейса к конкретному гейту."""
    pass

class MaintenanceRequiredException(AirportException):
    """Выбрасывается при попытке отправить в рейс борт, не прошедший технический осмотр."""
    pass

class NoAvailableCrewException(AirportException):
    """Выбрасывается при нехватке пилотов или бортпроводников для формирования экипажа."""
    pass

class WeatherWarningException(AirportException):
    """Выбрасывается диспетчерской вышкой при запрете вылетов из-за плохих метеоусловий."""
    pass

class CapacityExceededException(AirportException):
    """Выбрасывается при попытке продать билет на полностью заполненный рейс или переполнить зал ожидания."""
    pass

class PassengerNotFoundException(AirportException):
    """Выбрасывается при поиске несуществующего пассажира в манифесте рейса."""
    pass