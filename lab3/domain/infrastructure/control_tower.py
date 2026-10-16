"""Модуль командно-диспетчерского пункта (вышки КДП) аэропорта."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import RunwayBusyException, WeatherWarningException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.infrastructure.runway import Runway


class ControlTower:
    """Диспетчерская вышка. Центральный орган управления воздушным движением.
    Отвечает за выдачу разрешений на взлет/посадку с учетом метеоусловий."""

    def __init__(self, tower_name: str = "Main ATC Tower") -> None:
        """Инициализирует экземпляр класса ControlTower."""
        self.tower_name = tower_name
        self._runways: list[Runway] = []
        self.weather_is_safe = True

    @property
    def runways(self) -> list[Runway]:
        """Возвращает значение атрибута runways."""
        return list(self._runways)

    def add_runway(self, runway: Runway) -> None:
        """Берет ВПП под управление вышки."""
        self._runways.append(runway)

    def update_weather(self, is_safe: bool) -> None:
        """Обновляет статус безопасности метеоусловий."""
        self.weather_is_safe = is_safe

    def request_takeoff(self, aircraft: Aircraft) -> Runway:
        """Запрашивает коридор для взлета."""
        if not self.weather_is_safe:
            raise WeatherWarningException("Взлет запрещен из-за сложных метеоусловий.")
        for runway in self._runways:
            if not runway.is_busy:
                runway.occupy(aircraft)
                return runway
        raise RunwayBusyException("Все ВПП заняты, ожидайте слота.")

    def request_landing(self, aircraft: Aircraft) -> Runway:
        """Запрашивает коридор для посадки."""
        if not self.weather_is_safe:
            raise WeatherWarningException(
                "Посадка запрещена (аэропорт закрыт по метеоусловиям)."
            )
        for runway in self._runways:
            if not runway.is_busy:
                runway.occupy(aircraft)
                return runway
        raise RunwayBusyException("Борт отправлен в зону ожидания: все ВПП заняты.")

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"ControlTower(name={self.tower_name!r}, runways={len(self._runways)}, safe={self.weather_is_safe})"
