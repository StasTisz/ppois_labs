from __future__ import annotations

import uuid
from datetime import UTC, datetime


class WeatherReport:
    def __init__(self, temperature_c: float, wind_speed_ms: float, visibility_m: float, is_stormy: bool) -> None:
        self.report_id = str(uuid.uuid4())
        self.timestamp = datetime.now(UTC)
        self.temperature_c = temperature_c
        self.wind_speed_ms = wind_speed_ms
        self.visibility_m = visibility_m
        self.is_stormy = is_stormy

    @property
    def is_safe_for_operations(self) -> bool:
        if self.is_stormy:
            return False
        if self.wind_speed_ms > 25.0:
            return False
        if self.visibility_m < 400.0:
            return False
        return True
