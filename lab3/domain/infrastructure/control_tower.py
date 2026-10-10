from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import RunwayBusyException, WeatherWarningException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.infrastructure.runway import Runway


class ControlTower:
    def __init__(self) -> None:
        self.tower_id = str(uuid.uuid4())
        self._runways: list[Runway] = []
        self.weather_is_safe = True

    def add_runway(self, runway: Runway) -> None:
        self._runways.append(runway)

    def update_weather(self, is_safe: bool) -> None:
        self.weather_is_safe = is_safe

    def request_takeoff(self, aircraft: Aircraft) -> Runway:
        if not self.weather_is_safe:
            raise WeatherWarningException("Взлет запрещен из-за сложных метеоусловий.")
        for runway in self._runways:
            if not runway.is_busy:
                runway.occupy(aircraft)
                return runway
        raise RunwayBusyException("Все ВПП заняты, ожидайте слота.")

    def request_landing(self, aircraft: Aircraft) -> Runway:
        if not self.weather_is_safe:
            raise WeatherWarningException("Посадка запрещена (аэропорт закрыт по метеоусловиям).")
        for runway in self._runways:
            if not runway.is_busy:
                runway.occupy(aircraft)
                return runway
        raise RunwayBusyException("Борт отправлен в зону ожидания: все ВПП заняты.")
