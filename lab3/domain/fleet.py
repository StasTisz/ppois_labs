"""
Модуль транспортного парка (флота) аэропорта.

Содержит иерархию классов для воздушных судов (пассажирских, грузовых, частных)
и наземной спецтехники (тягачи, заправщики, автобусы). Обеспечивает полиморфизм
в процедурах технического обслуживания и инкапсуляцию внутренних состояний
(топливо, загрузка, пассажиры).
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from lab3.domain.exceptions import CapacityExceededException


class Vehicle(ABC):
    """
    Базовый абстрактный класс для любого транспортного средства в аэропорту.
    Определяет общий контракт технического обслуживания.

    Attributes:
        vehicle_id (str): Внутренний уникальный идентификатор транспорта.
        model (str): Модель транспортного средства (например, "Boeing 737").
        max_speed (float): Максимальная скорость в км/ч.
        requires_maintenance (bool): Флаг необходимости проведения ТО.
        operating_hours (float): Количество часов наработки после последнего ТО.
    """

    def __init__(self, model: str, max_speed: float) -> None:
        self.vehicle_id = str(uuid.uuid4())
        self.model = model
        self.max_speed = max_speed
        self.requires_maintenance = False
        self.operating_hours = 0.0

    @abstractmethod
    def perform_maintenance(self) -> None:
        """
        Полиморфный контракт проведения ТО.
        Каждый конкретный тип техники реализует свои уникальные процедуры.
        """


class Aircraft(Vehicle, ABC):
    """
    Абстрактный класс воздушного судна.
    Отвечает за базовые механики полета и заправки.

    Attributes:
        tail_number (str): Бортовой регистрационный номер (например, "RA-12345").
        fuel_capacity (float): Максимальный объем топливных баков в литрах.
        is_in_flight (bool): Находится ли судно в данный момент в воздухе.
    """

    def __init__(self, model: str, max_speed: float, tail_number: str, fuel_capacity: float) -> None:
        super().__init__(model, max_speed)
        self.tail_number = tail_number
        self.fuel_capacity = fuel_capacity
        self._current_fuel = 0.0  # Защищенное поле, меняется только через refuel()
        self.is_in_flight = False

    @property
    def current_fuel(self) -> float:
        """Текущий уровень топлива в баках (доступно только для чтения)."""
        return self._current_fuel

    def refuel(self, amount: float) -> None:
        """
        Заправляет самолет указанным объемом топлива.

        Raises:
            ValueError: При попытке залить отрицательный объем.
            CapacityExceededException: При превышении емкости баков.
        """
        if amount <= 0:
            raise ValueError("Объем заправки должен быть положительным.")
        if self._current_fuel + amount > self.fuel_capacity:
            raise CapacityExceededException(f"Баки переполнены. Максимум: {self.fuel_capacity} л.")
        self._current_fuel += amount

    def take_off(self) -> None:
        """Переводит борт в статус полета."""
        self.is_in_flight = True

    def land(self) -> None:
        """
        Регистрирует приземление борта.
        После каждого рейса автоматически выставляется флаг необходимости ТО.
        """
        self.is_in_flight = False
        self.requires_maintenance = True


class PassengerAircraft(Aircraft):
    """
    Пассажирский лайнер. Управляет посадкой людей и системами жизнеобеспечения.
    """

    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, max_passengers: int
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_passengers = max_passengers
        self._passengers_count = 0
        self.oxygen_masks_tested = False
        self.cabin_pressurization_ok = True

    @property
    def passengers_count(self) -> int:
        """Текущее количество пассажиров на борту (доступно только для чтения)."""
        return self._passengers_count

    def board_passengers(self, count: int) -> None:
        """Осуществляет посадку пассажиров с проверкой вместимости салона."""
        if self._passengers_count + count > self.max_passengers:
            raise CapacityExceededException("Количество пассажиров превышает вместимость салона.")
        self._passengers_count += count

    def disembark_passengers(self) -> int:
        """Высаживает всех пассажиров и возвращает их количество."""
        count = self._passengers_count
        self._passengers_count = 0
        return count

    def perform_maintenance(self) -> None:
        """ТО пассажирского лайнера: проверка кислородных систем и герметичности."""
        self.oxygen_masks_tested = True
        self.cabin_pressurization_ok = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class CargoAircraft(Aircraft):
    """
    Грузовой самолет. Оперирует весом груза и механизмами рампы.
    """

    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, max_payload_kg: float
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_payload_kg = max_payload_kg
        self._current_payload_kg = 0.0
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = False

    @property
    def current_payload_kg(self) -> float:
        """Текущий вес загруженного груза в килограммах (доступно только для чтения)."""
        return self._current_payload_kg

    def load_cargo(self, weight: float) -> None:
        """Загружает карго с проверкой максимальной грузоподъемности."""
        if self._current_payload_kg + weight > self.max_payload_kg:
            raise CapacityExceededException("Перевес: превышена максимальная грузоподъемность.")
        self._current_payload_kg += weight

    def unload_cargo(self) -> float:
        """Полностью выгружает карго-трюм."""
        weight = self._current_payload_kg
        self._current_payload_kg = 0.0
        return weight

    def perform_maintenance(self) -> None:
        """ТО грузового борта: диагностика гидравлики рампы и лебедки."""
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class PrivateJet(Aircraft):
    """
    Частный бизнес-джет. Включает сервисы VIP-кейтеринга и спутниковую связь.
    """

    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, owner_name: str
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.owner_name = owner_name
        self.is_vip_catered = False
        self.satellite_comms_calibrated = False

    def order_vip_catering(self) -> None:
        """Заказывает премиальное бортовое питание."""
        self.is_vip_catered = True

    def perform_maintenance(self) -> None:
        """ТО бизнес-джета: калибровка спутниковой связи."""
        self.satellite_comms_calibrated = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class GroundVehicle(Vehicle, ABC):
    """
    Базовый абстрактный класс наземной спецтехники перрона.

    Attributes:
        license_plate (str): Регистрационный номер машины.
        is_available (bool): Статус доступности для новых задач диспетчера.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed)
        self.license_plate = license_plate
        self.is_available = True

    def dispatch(self) -> None:
        """Отправляет технику на задание, блокируя её статус."""
        if not self.is_available:
            raise ValueError(f"Техника {self.license_plate} уже занята.")
        self.is_available = False

    def release(self) -> None:
        """Освобождает технику после выполнения задачи."""
        self.is_available = True


class BaggageTractor(GroundVehicle):
    """
    Багажный тягач. Перевозит тележки с чемоданами между терминалом и бортом.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str, max_carts: int = 4) -> None:
        super().__init__(model, max_speed, license_plate)
        self.max_carts = max_carts
        self._current_carts = 0
        self.tow_hitch_greased = False

    @property
    def current_carts(self) -> int:
        """Текущее количество прицепленных тележек."""
        return self._current_carts

    def attach_cart(self) -> None:
        """Прицепляет дополнительную багажную тележку."""
        if self._current_carts >= self.max_carts:
            raise CapacityExceededException("Достигнут лимит багажных тележек.")
        self._current_carts += 1

    def detach_all_carts(self) -> None:
        """Отцепляет все тележки."""
        self._current_carts = 0

    def perform_maintenance(self) -> None:
        """ТО тягача: смазка сцепки и проверка тормозного контура тележек."""
        self.tow_hitch_greased = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class FuelTruck(GroundVehicle):
    """
    Автомобиль-топливозаправщик. Перекачивает топливо в баки судов.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str, tank_capacity: float) -> None:
        super().__init__(model, max_speed, license_plate)
        self.tank_capacity = tank_capacity
        self._current_fuel = tank_capacity  # Выезжает с полным баком
        self.pump_calibrated = False
        self.filter_replaced = False

    @property
    def current_fuel(self) -> float:
        """Текущий остаток топлива в цистерне заправщика."""
        return self._current_fuel

    def refuel_aircraft(self, aircraft: Aircraft, amount: float) -> None:
        """
        Перекачивает керосин из цистерны грузовика в баки самолета.

        Args:
            aircraft (Aircraft): Борт, который необходимо заправить.
            amount (float): Объем перекачиваемого топлива.
        """
        if self._current_fuel < amount:
            raise CapacityExceededException("В цистерне топливозаправщика недостаточно керосина.")

        self.dispatch()
        aircraft.refuel(amount)
        self._current_fuel -= amount
        self.release()

    def perform_maintenance(self) -> None:
        """ТО заправщика: регламентная замена фильтров и калибровка счетчика."""
        self.pump_calibrated = True
        self.filter_replaced = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class FollowMeCar(GroundVehicle):
    """
    Машина сопровождения эскорта (Follow Me Car).
    """

    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed, license_plate)
        self.lightbar_tested = False

    def lead_aircraft(self, aircraft: Aircraft, destination: str) -> str:
        """Сопровождает самолет до заданной точки (гейта или ВПП)."""
        self.dispatch()
        result = f"Борт {aircraft.tail_number} успешно сопровожден к: {destination}"
        self.release()
        return result

    def perform_maintenance(self) -> None:
        """ТО машины эскорта: тест светодиодного табло и радиостанции."""
        self.lightbar_tested = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class PassengerBus(GroundVehicle):
    """
    Перронный автобус. Осуществляет трансфер пассажиров к трапу самолета.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str, capacity: int) -> None:
        super().__init__(model, max_speed, license_plate)
        self.capacity = capacity
        self._passengers_count = 0
        self.doors_pneumatics_checked = False

    @property
    def passengers_count(self) -> int:
        """Текущее количество пассажиров в салоне."""
        return self._passengers_count

    def board(self, count: int) -> None:
        """Загружает пассажиров в салон автобуса."""
        if self._passengers_count + count > self.capacity:
            raise CapacityExceededException("Перронный автобус переполнен.")
        self._passengers_count += count

    def drop_off(self) -> int:
        """Высаживает пассажиров у трапа или терминала."""
        count = self._passengers_count
        self._passengers_count = 0
        return count

    def perform_maintenance(self) -> None:
        """ТО автобуса: ревизия пневматики дверей и аппарелей."""
        self.doors_pneumatics_checked = True
        self.requires_maintenance = False
        self.operating_hours = 0.0