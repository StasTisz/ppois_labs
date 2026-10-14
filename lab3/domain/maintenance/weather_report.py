from __future__ import annotations

from datetime import UTC, datetime


class WeatherReport:
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
        self.station_code = station_code
        self.temperature_c = temperature_c
        self.wind_speed_ms = wind_speed_ms
        self.visibility_m = visibility_m
        self.is_stormy = is_stormy
        self.recorded_at = datetime.now(UTC)

    @property
    def is_safe_for_operations(self) -> bool:
        if self.is_stormy:
            return False
        if self.wind_speed_ms > self.MAX_SAFE_WIND_SPEED_MS:
            return False
        return self.visibility_m >= self.MIN_SAFE_VISIBILITY_M

    def is_acceptable_for_takeoff(self) -> bool:
        return self.is_safe_for_operations

    def update_conditions(
        self,
        temperature_c: float,
        wind_speed_ms: float,
        visibility_m: float,
        is_stormy: bool,
    ) -> None:
        self.temperature_c = temperature_c
        self.wind_speed_ms = wind_speed_ms
        self.visibility_m = visibility_m
        self.is_stormy = is_stormy
        self.recorded_at = datetime.now(UTC)

    def format_metar(self) -> str:
        storm_flag = "TS" if self.is_stormy else "NOSIG"
        return f"METAR {self.station_code} {int(self.temperature_c)}C WIND {self.wind_speed_ms}MPS VIS {int(self.visibility_m)}M {storm_flag}"

    def __repr__(self) -> str:
        return f"WeatherReport(station={self.station_code!r}, safe={self.is_safe_for_operations})"
