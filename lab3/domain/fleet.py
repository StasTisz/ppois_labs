import uuid
from abc import ABC, abstractmethod

from lab3.domain.exceptions import CapacityExceededException


class Vehicle(ABC):
    """
    Базовый абстрактный класс для любого транспортного средства в аэропорту.
    """

    def __init__(self, model: str, max_speed: float) -> None:
        self.vehicle_id = str(uuid.uuid4())
        self.model = model
        self.max_speed = max_speed
        self.requires_maintenance = False
        self.operating_hours = 0.0

    @abstractmethod
    def perform_maintenance(self) -> None:
        """Полиморфный контракт проведения ТО."""
        pass


class Aircraft(Vehicle, ABC):
    """
    Абстрактный класс воздушного судна.
    """

    def __init__(self, model: str, max_speed: float, tail_number: str, fuel_capacity: float) -> None:
        super().__init__(model, max_speed)
        self.tail_number = tail_number
        self.fuel_capacity = fuel_capacity
        self.current_fuel = 0.0
        self.is_in_flight = False

    def refuel(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Объем заправки должен быть положительным.")
        if self.current_fuel + amount > self.fuel_capacity:
            raise CapacityExceededException(f"Баки переполнены. Максимум: {self.fuel_capacity} л.")
        self.current_fuel += amount

    def take_off(self) -> None:
        self.is_in_flight = True

    def land(self) -> None:
        self.is_in_flight = False
        self.requires_maintenance = True


class PassengerAircraft(Aircraft):
    """
    Пассажирский лайнер с контролем систем жизнеобеспечения.
    """

    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, max_passengers: int
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_passengers = max_passengers
        self.passengers_count = 0
        self.oxygen_masks_tested = False
        self.cabin_pressurization_ok = True

    def board_passengers(self, count: int) -> None:
        if self.passengers_count + count > self.max_passengers:
            raise CapacityExceededException("Количество пассажиров превышает вместимость салона.")
        self.passengers_count += count

    def disembark_passengers(self) -> int:
        count = self.passengers_count
        self.passengers_count = 0
        return count

    def perform_maintenance(self) -> None:
        """Реальное ТО лайнера: проверка кислородных систем и герметичности салона."""
        self.oxygen_masks_tested = True
        self.cabin_pressurization_ok = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class CargoAircraft(Aircraft):
    """
    Грузовой самолет с проверкой гидроприводов рампы и швартовки.
    """

    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, max_payload_kg: float
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_payload_kg = max_payload_kg
        self.current_payload_kg = 0.0
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = False

    def load_cargo(self, weight: float) -> None:
        if self.current_payload_kg + weight > self.max_payload_kg:
            raise CapacityExceededException("Перевес: превышена максимальная грузоподъемность.")
        self.current_payload_kg += weight

    def unload_cargo(self) -> float:
        weight = self.current_payload_kg
        self.current_payload_kg = 0.0
        return weight

    def perform_maintenance(self) -> None:
        """ТО грузового борта: диагностика гидравлики рампы и лебедки."""
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class PrivateJet(Aircraft):
    """
    Бизнес-джет с диагностикой спутниковой авионики.
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
        self.is_vip_catered = True

    def perform_maintenance(self) -> None:
        """ТО бизнес-джета: калибровка спутниковой связи и сервисных систем."""
        self.satellite_comms_calibrated = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class GroundVehicle(Vehicle, ABC):
    """
    Абстрактный класс наземной спецтехники перрона.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed)
        self.license_plate = license_plate
        self.is_available = True

    def dispatch(self) -> None:
        if not self.is_available:
            raise ValueError(f"Техника {self.license_plate} уже занята.")
        self.is_available = False

    def release(self) -> None:
        self.is_available = True


class BaggageTractor(GroundVehicle):
    """
    Багажный тягач с проверкой сцепных устройств.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str, max_carts: int = 4) -> None:
        super().__init__(model, max_speed, license_plate)
        self.max_carts = max_carts
        self.current_carts = 0
        self.tow_hitch_greased = False

    def attach_cart(self) -> None:
        if self.current_carts >= self.max_carts:
            raise CapacityExceededException("Достигнут лимит багажных тележек.")
        self.current_carts += 1

    def detach_all_carts(self) -> None:
        self.current_carts = 0

    def perform_maintenance(self) -> None:
        """ТО тягача: смазка сцепки и проверка тормозного контура тележек."""
        self.tow_hitch_greased = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class FuelTruck(GroundVehicle):
    """
    Топливозаправщик с заменой топливных фильтров и калибровкой насоса.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str, tank_capacity: float) -> None:
        super().__init__(model, max_speed, license_plate)
        self.tank_capacity = tank_capacity
        self.current_fuel = tank_capacity
        self.pump_calibrated = False
        self.filter_replaced = False

    def refuel_aircraft(self, aircraft: Aircraft, amount: float) -> None:
        if self.current_fuel < amount:
            raise CapacityExceededException("В цистерне топливозаправщика недостаточно керосина.")
        self.dispatch()
        aircraft.refuel(amount)
        self.current_fuel -= amount
        self.release()

    def perform_maintenance(self) -> None:
        """ТО заправщика: регламентная замена фильтров и калибровка счетчика."""
        self.pump_calibrated = True
        self.filter_replaced = True
        self.requires_maintenance = False
        self.operating_hours = 0.0


class FollowMeCar(GroundVehicle):
    """
    Машина сопровождения с проверкой сигнального светового табло.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed, license_plate)
        self.lightbar_tested = False

    def lead_aircraft(self, aircraft: Aircraft, destination: str) -> str:
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
    Перронный автобус с проверкой пневмопривода дверей.
    """

    def __init__(self, model: str, max_speed: float, license_plate: str, capacity: int) -> None:
        super().__init__(model, max_speed, license_plate)
        self.capacity = capacity
        self.passengers_count = 0
        self.doors_pneumatics_checked = False

    def board(self, count: int) -> None:
        if self.passengers_count + count > self.capacity:
            raise CapacityExceededException("Перронный автобус переполнен.")
        self.passengers_count += count

    def drop_off(self) -> int:
        count = self.passengers_count
        self.passengers_count = 0
        return count

    def perform_maintenance(self) -> None:
        """ТО автобуса: ревизия пневматики дверей и аппарелей для маломобильных граждан."""
        self.doors_pneumatics_checked = True
        self.requires_maintenance = False
        self.operating_hours = 0.0