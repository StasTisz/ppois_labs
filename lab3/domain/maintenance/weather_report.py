"""Модуль метеорологической сводки аэропорта."""

from __future__ import annotations

from datetime import UTC, datetime


class WeatherReport:
    """Метеорологическая сводка аэропорта.
    Служит источником правды для диспетчерской вышки при выдаче разрешений."""

    MAX_SAFE_WIND_SPEED_MS = 25.0
    MIN_SAFE_VISIBILITY_M = 500.0

    def __init__(
        self,
        temperature_c: float,
        wind_speed_ms: float,
        visibility_m: float,
        is_stormy: bool,
        station_code: str = "UMMS",
    ) -> None:
        """Инициализирует экземпляр класса WeatherReport."""
        self.station_code = station_code
        self.temperature_c = temperature_c
        self.wind_speed_ms = wind_speed_ms
        self.visibility_m = visibility_m
        self.is_stormy = is_stormy
        self.recorded_at = datetime.now(UTC)

    @property
    def is_safe_for_operations(self) -> bool:
        """Анализирует параметры погоды и определяет, безопасны ли условия
        для взлета, посадки и перронных работ."""
        if self.is_stormy:
            return False
        if self.wind_speed_ms > self.MAX_SAFE_WIND_SPEED_MS:
            return False
        return self.visibility_m >= self.MIN_SAFE_VISIBILITY_M

    def is_acceptable_for_takeoff(self) -> bool:
        """Оценивает метеоусловия на предмет допустимости взлета судна."""
        return self.is_safe_for_operations

    def update_conditions(
        self,
        temperature_c: float,
        wind_speed_ms: float,
        visibility_m: float,
        is_stormy: bool,
    ) -> None:
        """Обновляет текущие метеорологические параметры атмосферы."""
        self.temperature_c = temperature_c
        self.wind_speed_ms = wind_speed_ms
        self.visibility_m = visibility_m
        self.is_stormy = is_stormy
        self.recorded_at = datetime.now(UTC)

    def format_metar(self) -> str:
        """Формирует стандартный авиационный отчет метеосводки в формате METAR."""
        storm_flag = "TS" if self.is_stormy else "NOSIG"
        return f"METAR {self.station_code} {int(self.temperature_c)}C WIND {self.wind_speed_ms}MPS VIS {int(self.visibility_m)}M {storm_flag}"

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"WeatherReport(station={self.station_code!r}, safe={self.is_safe_for_operations})"
