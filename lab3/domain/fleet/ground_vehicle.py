"""Модуль базового аэродромного наземного спецтранспорта."""

from __future__ import annotations

from lab3.domain.fleet.vehicle import Vehicle


class GroundVehicle(Vehicle):
    """Базовый абстрактный класс наземной спецтехники перрона."""

    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        """Инициализирует экземпляр класса GroundVehicle."""
        super().__init__(model, max_speed)
        self.license_plate = license_plate
        self.is_dispatched = False

    @property
    def is_available(self) -> bool:
        """Возвращает признак available."""
        return not self.is_dispatched

    def dispatch(self) -> None:
        """Отправляет технику на задание, блокируя её статус."""
        if self.is_dispatched:
            raise ValueError(
                f"Транспорт {self.license_plate} уже отправлен на задание."
            )
        self.is_dispatched = True

    def release(self) -> None:
        """Освобождает технику после выполнения задачи."""
        self.is_dispatched = False

    def perform_maintenance(self) -> None:
        """Выполняет регламентное техническое обслуживание наземного спецавтомобиля."""
        self.requires_maintenance = False

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"{self.__class__.__name__}(plate={self.license_plate!r}, model={self.model!r})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, GroundVehicle):
            return NotImplemented
        return self.license_plate == other.license_plate

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.license_plate)
