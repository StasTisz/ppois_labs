"""Консольный интерфейс (CLI) для информационной системы аэропорта (Лаба №3).

Обеспечивает интерактивное управление всеми доменами:
1. Флот и техника (fleet/) - добавление/удаление самолетов и спецтехники, полиморфные операции
2. Инфраструктура (infrastructure/) - терминалы, гейты, ВПП, ангар, парковка, бизнес-зал
3. Персонал и пассажиры (people/) - наем/увольнение экипажа и служб, смены
4. Операционная деятельность (operations/) - табло, билеты, регистрация, багаж
5. Служба безопасности (security/) - металлодетекторы, интроскопы, паспортный и таможенный контроль
6. Наземное обслуживание (maintenance/) - полиморфные задачи ТО, заправка, клининг, кейтеринг
7. Фасад аэропорта (facade/) - комплексный автоматизированный цикл рейса
"""

from __future__ import annotations

import os
import pickle
import sys
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from lab3.domain.exceptions import AirportException
from lab3.domain.facade import AirportFacade
from lab3.domain.fleet import (
    Aircraft,
    BaggageTractor,
    CargoAircraft,
    FollowMeCar,
    FuelTruck,
    GroundVehicle,
    PassengerAircraft,
    PassengerBus,
    PrivateJet,
)
from lab3.domain.infrastructure import Gate, Hangar, Lounge, ParkingLot, Runway, Terminal
from lab3.domain.maintenance import (
    CateringTask,
    CleaningTask,
    MaintenanceInspection,
    RefuelingTask,
    ServiceTask,
    WeatherReport,
)
from lab3.domain.operations import Baggage
from lab3.domain.people import (
    BaggageHandler,
    CheckInAgent,
    Dispatcher,
    Employee,
    FlightAttendant,
    Passenger,
    Pilot,
    SecurityOfficer,
)
from lab3.domain.security import (
    CustomsControl,
    CustomsDeclaration,
    MetalDetector,
    PassportControl,
    Visa,
    XRayScanner,
)

DEFAULT_STATE_FILE = "lab3_state.pkl"


def _prompt(text: str, default: str = "") -> str:
    prompt_str = f"{text} [{default}]: " if default else f"{text}: "
    val = input(prompt_str).strip()
    return val if val else default


def _prompt_int(text: str, default: int) -> int:
    val = _prompt(text, str(default))
    try:
        return int(val)
    except ValueError:
        return default


def _prompt_float(text: str, default: float) -> float:
    val = _prompt(text, str(default))
    try:
        return float(val)
    except ValueError:
        return default


class DataSeeder:
    """Генератор стартовых данных для аэропорта."""

    @staticmethod
    def _seed_base() -> tuple[AirportFacade, Gate, Runway, Hangar, ParkingLot, Lounge]:
        facade = AirportFacade("Национальный аэропорт Минск", "MSQ")
        term = Terminal("Терминал 1")
        gate_a1 = Gate("A1")
        term.add_gate(gate_a1)
        lounge = Lounge("VIP Lounge", capacity=20, is_vip=True)
        term.add_lounge(lounge)
        facade.airport.add_terminal(term)
        rw1 = Runway("12L", 3600)
        facade.airport.control_tower.add_runway(rw1)
        hangar = Hangar(1, capacity=3)
        parking = ParkingLot("P1", total_spaces=10)
        return facade, gate_a1, rw1, hangar, parking, lounge

    @staticmethod
    def _seed_fleet(facade: AirportFacade) -> tuple[PassengerAircraft, CargoAircraft, list[GroundVehicle], FuelTruck]:
        plane_p = PassengerAircraft("Boeing 737-800", 850.0, "EW-737MS", 18000.0, 189)
        plane_c = CargoAircraft("Ил-76ТД", 750.0, "EW-76CARGO", 25000.0, 48000.0)
        facade.register_aircraft(plane_p)
        facade.register_aircraft(plane_c)
        bus = PassengerBus("МАЗ-171", 50.0, "BUS-01", passenger_capacity=100)
        tractor = BaggageTractor("TUG-Alpha", 30.0, "TR-01", max_carts=4)
        truck = FuelTruck("Scania P410", 60.0, "FT-01", tank_capacity=20000.0)
        follow = FollowMeCar("Skoda Octavia", 120.0, "FM-01")
        facade.register_fuel_truck(truck)
        return plane_p, plane_c, [bus, tractor, truck, follow], truck

    @staticmethod
    def _seed_people_and_flight(
        facade: AirportFacade, plane: PassengerAircraft, gate: Gate
    ) -> tuple[Pilot, BaggageHandler, SecurityOfficer, Passenger]:
        pilot = Pilot("Иван", "Капитан", "PP-101", 5500.0, "ATPL", is_captain=True)
        handler = BaggageHandler("Петр", "Грузчиков", "BH-202", 2100.0)
        sec = SecurityOfficer("Ольга", "Досмотрова", "SEC-303", 2200.0)
        for emp in (pilot, handler, sec):
            emp.clock_in()
            facade.register_employee(emp)
        facade.checkpoint.assign_officer(sec)
        passr = Passenger("Дмитрий", "Пассажиров", "KH777888")
        facade.register_passenger(passr.first_name, passr.last_name, passr.passport_number)
        dep_time = datetime.now(UTC) + timedelta(hours=2)
        flight = facade.create_departure_flight("B2-990", "Belavia", plane.tail_number, "MSQ", "DXB", dep_time)
        flight.assign_gate(gate)
        return pilot, handler, sec, passr

    @staticmethod
    def seed() -> dict:
        facade, gate, rw, hangar, parking, lounge = DataSeeder._seed_base()
        p_p, p_c, vehicles, truck = DataSeeder._seed_fleet(facade)
        pilot, handler, sec, passr = DataSeeder._seed_people_and_flight(facade, p_p, gate)
        d = {"facade": facade, "gate": gate, "rw": rw, "hangar": hangar, "parking": parking, "lounge": lounge}
        d.update({"plane_p": p_p, "plane_c": p_c, "vehicles": vehicles, "truck": truck})
        d.update({"pilot": pilot, "handler": handler, "sec": sec, "passr": passr})
        return d


class CLI:
    """Интерактивный консольный интерфейс аэропорта (Лаба №3)."""

    def __init__(self, state_file: str = DEFAULT_STATE_FILE) -> None:
        self.state_file = state_file
        print("Инициализация доменной модели аэропорта... Загрузка.")
        self.state = DataSeeder.seed()
        self.facade: AirportFacade = self.state["facade"]

    def save_state(self) -> None:
        with open(self.state_file, "wb") as f:
            pickle.dump(self.state, f)
        print(f"💾 Состояние аэропорта сохранено в '{self.state_file}'.")

    def load_state(self) -> bool:
        if not os.path.exists(self.state_file):
            print(f"⚠️ Файл '{self.state_file}' не найден.")
            return False
        with open(self.state_file, "rb") as f:
            self.state = pickle.load(f)
        self.facade = self.state["facade"]
        print(f"📂 Состояние аэропорта восстановлено из '{self.state_file}'.")
        return True

    def _show_fleet(self) -> None:
        print(f"\n✈️ Воздушные суда ({len(self.facade.aircrafts)}):")
        for a in self.facade.aircrafts:
            print(f" └─ [{type(a).__name__}] {a.model} ({a.tail_number}) | Топливо: {a.current_fuel}/{a.fuel_capacity} л")
        vehicles: list[GroundVehicle] = self.state["vehicles"]
        print(f"\n🚜 Перронная спецтехника ({len(vehicles)}):")
        for v in vehicles:
            print(f" └─ [{type(v).__name__}] {v.model} ({v.license_plate}) | Скорость: {v.max_speed} км/ч | Доступен: {v.is_available}")

    def _add_aircraft(self) -> None:
        print("Тип: 1. Пассажирский (PassengerAircraft)  2. Грузовой (CargoAircraft)  3. Бизнес-джет (PrivateJet)")
        choice = _prompt("Выбор типа", "1")
        model = _prompt("Модель судна", "Airbus A320")
        tail = _prompt("Бортовой номер", f"EW-{_prompt_int('Число в номере', 320)}AR")
        plane: Aircraft
        if choice == "2":
            plane = CargoAircraft(model, 780.0, tail, 22000.0, max_payload_kg=35000.0)
        elif choice == "3":
            plane = PrivateJet(model, 880.0, tail, 12000.0, owner_name="VIP Client")
        else:
            plane = PassengerAircraft(model, 840.0, tail, 16000.0, seating_capacity=160)
        self.facade.register_aircraft(plane)
        print(f"✅ Добавлен борт [{type(plane).__name__}] {model} ({tail}).")

    def _remove_aircraft(self) -> None:
        tail = _prompt("Бортовой номер судна для списания", "EW-76CARGO")
        plane = self.facade.find_aircraft(tail)
        if not plane:
            print("❌ Борт с таким номером не найден.")
            return
        self.facade.aircrafts.remove(plane)
        print(f"✅ Самолет {tail} списан из флота аэропорта.")

    def _add_vehicle(self) -> None:
        print("Тип: 1. Автобус (PassengerBus)  2. Тягач (BaggageTractor)  3. Заправщик (FuelTruck)  4. Follow-Me")
        choice = _prompt("Выбор типа", "1")
        plate = _prompt("Номерной знак", f"TECH-{_prompt_int('Индекс', 10)}")
        model = _prompt("Марка техники", "BelAZ-Service")
        veh: GroundVehicle
        if choice == "2":
            veh = BaggageTractor(model, 35.0, plate, max_carts=5)
        elif choice == "3":
            veh = FuelTruck(model, 60.0, plate, tank_capacity=15000.0)
            self.facade.register_fuel_truck(veh)
        elif choice == "4":
            veh = FollowMeCar(model, 110.0, plate)
        else:
            veh = PassengerBus(model, 50.0, plate, passenger_capacity=90)
        self.state["vehicles"].append(veh)
        print(f"✅ Добавлена техника [{type(veh).__name__}] {model} ({plate}).")

    def _remove_vehicle(self) -> None:
        plate = _prompt("Номерной знак спецтехники", "BUS-01")
        vehicles: list[GroundVehicle] = self.state["vehicles"]
        target = next((v for v in vehicles if v.license_plate == plate), None)
        if not target:
            print("❌ Техника не найдена.")
            return
        vehicles.remove(target)
        print(f"✅ Техника {plate} списана из автопарка.")

    def _run_bus_or_tractor(self, ch: str, vehicles: list[GroundVehicle], p: Passenger) -> None:
        if ch == "1":
            bus = next((v for v in vehicles if isinstance(v, PassengerBus)), None)
            if bus:
                bus.board_passenger(p)
                print(f"🚌 {p.full_name} сел в автобус {bus.model}. Пассажиров: {bus.passengers_count}.")
        elif ch == "2":
            tr = next((v for v in vehicles if isinstance(v, BaggageTractor)), None)
            if tr:
                tr.transport_baggage(Baggage(15.0, p, "TAG-TR"))
                print(f"🚜 Тягач {tr.model}: багаж доставлен. Прицепов: {tr.current_carts}.")

    def _run_truck_or_follow(self, ch: str, vehicles: list[GroundVehicle], plane: Aircraft) -> None:
        if ch == "3":
            truck = next((v for v in vehicles if isinstance(v, FuelTruck)), None)
            if truck:
                truck.refuel_aircraft(plane, 2000.0)
                print(f"⛽ Заправщик {truck.model}: борт заправлен ({plane.current_fuel} л).")
        elif ch == "4":
            fm = next((v for v in vehicles if isinstance(v, FollowMeCar)), None)
            if fm:
                print(f"🚨 {fm.lead_aircraft(plane, 'Stand 4')}")

    def _run_vehicle_operation(self) -> None:
        print("\n⚡ Демонстрация полиморфизма техники:")
        print("1. Посадка в автобус (PassengerBus)    2. Доставка сумок тягачом (BaggageTractor)")
        print("3. Дозаправка баков (FuelTruck)        4. Сопровождение борта (FollowMeCar)")
        ch = _prompt("Выбор", "1")
        vehicles: list[GroundVehicle] = self.state["vehicles"]
        p: Passenger = self.state["passr"]
        plane: Aircraft = self.facade.aircrafts[0]
        if ch in ("1", "2"):
            self._run_bus_or_tractor(ch, vehicles, p)
        elif ch in ("3", "4"):
            self._run_truck_or_follow(ch, vehicles, plane)

    def _menu_fleet(self) -> None:
        acts: dict[str, Callable[[], None]] = {
            "1": self._show_fleet, "2": self._add_aircraft, "3": self._remove_aircraft,
            "4": self._add_vehicle, "5": self._remove_vehicle, "6": self._run_vehicle_operation,
        }
        while True:
            print("\n--- ✈️ ФЛОТ И СПЕЦТЕХНИКА (fleet/) ---")
            print("1. Список флота и техники\n2. Добавить самолет\n3. Удалить самолет")
            print("4. Добавить технику\n5. Удалить технику\n6. Запустить действие\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch in acts:
                acts[ch]()
            elif ch == "0":
                break

    def _show_infrastructure(self) -> None:
        term = self.facade.airport.terminals[0]
        tower = self.facade.airport.control_tower
        hangar: Hangar = self.state["hangar"]
        parking: ParkingLot = self.state["parking"]
        lounge: Lounge = self.state["lounge"]
        print(f"\n🏢 Терминал: {term.name} | Гейтов: {len(term.gates)} | Лаунжей: {len(term.lounges)}")
        print(f"🗼 Диспетчерская вышка: Полос (ВПП): {len(tower.runways)}")
        for rw in tower.runways:
            busy = f"Занята ({rw.current_aircraft.tail_number})" if rw.is_busy and rw.current_aircraft else "Свободна"
            print(f" └─ ВПП {rw.number} (длина {rw.length}м): {busy}")
        print(f"🔧 Ангар #{hangar.number}: занято {hangar.current_occupancy}/{hangar.capacity}")
        print(f"🅿️ Парковка '{parking.zone_code}': занято {parking.parked_vehicles_count}/{parking.total_spaces}")
        print(f"☕ Лаунж '{lounge.name}': гостей {lounge.current_occupancy}/{lounge.capacity}")

    def _add_gate(self) -> None:
        g_num = _prompt("Номер нового гейта", "B2")
        gate = Gate(g_num)
        self.facade.airport.terminals[0].add_gate(gate)
        print(f"✅ Гейт {g_num} успешно привязан к Терминалу 1.")

    def _add_runway(self) -> None:
        num = _prompt("Обозначение ВПП", "30R")
        length = _prompt_int("Длина полосы в метрах", 3800)
        rw = Runway(num, length)
        self.facade.airport.control_tower.add_runway(rw)
        print(f"✅ Взлетно-посадочная полоса {num} введена в эксплуатацию.")

    def _hangar_operations(self) -> None:
        hangar: Hangar = self.state["hangar"]
        plane: Aircraft = self.facade.aircrafts[0]
        print("1. Закатить самолет в ангар  2. Выкатить самолет из ангара")
        ch = _prompt("Выбор", "1")
        if ch == "1":
            hangar.store_aircraft(plane)
            print(f"✅ Борт {plane.tail_number} помещен в ангар на обслуживание.")
        else:
            hangar.release_aircraft(plane)
            print(f"✅ Борт {plane.tail_number} выкачен из ангара на перрон.")

    def _parking_operations(self) -> None:
        parking: ParkingLot = self.state["parking"]
        veh: GroundVehicle = self.state["vehicles"][0]
        print("1. Припарковать спецтехнику  2. Забрать спецтехнику со стоянки")
        ch = _prompt("Выбор", "1")
        if ch == "1":
            parking.park_car(veh)
            print(f"✅ Автомобиль {veh.license_plate} припаркован на стоянке {parking.zone_code}.")
        else:
            parking.remove_car(veh)
            print(f"✅ Автомобиль {veh.license_plate} покинул стоянку {parking.zone_code}.")

    def _lounge_operations(self) -> None:
        lounge: Lounge = self.state["lounge"]
        p: Passenger = self.state["passr"]
        print("1. Впустить пассажира в VIP-зал  2. Пассажир покидает VIP-зал")
        ch = _prompt("Выбор", "1")
        if ch == "1":
            lounge.enter(p)
            print(f"✅ Пассажир {p.full_name} зашел в {lounge.name}.")
        else:
            lounge.exit(p)
            print(f"✅ Пассажир {p.full_name} покинул {lounge.name}.")

    def _menu_infrastructure(self) -> None:
        acts: dict[str, Callable[[], None]] = {
            "1": self._show_infrastructure, "2": self._add_gate, "3": self._add_runway,
            "4": self._hangar_operations, "5": self._parking_operations, "6": self._lounge_operations,
        }
        while True:
            print("\n--- 🏢 ИНФРАСТРУКТУРА АЭРОПОРТА (infrastructure/) ---")
            print("1. Обзор\n2. Добавить гейт\n3. Добавить ВПП\n4. Ангар\n5. Парковка\n6. VIP-зал\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch in acts:
                acts[ch]()
            elif ch == "0":
                break

    def _show_people(self) -> None:
        print(f"\n👔 Персонал аэропорта ({len(self.facade.employees)}):")
        for e in self.facade.employees:
            stat = "🟢 На смене" if e.is_on_shift else "⚪ Отдыхает"
            print(f" └─ [{type(e).__name__}] {e.full_name} | ID: {e.employee_id} | Оклад: {e.salary} BYN | {stat}")
        print(f"\n🧳 Зарегистрированные пассажиры ({len(self.facade.passengers)}):")
        for p in self.facade.passengers:
            print(f" └─ {p.full_name} | Паспорт: {p.passport_number}")

    def _add_employee(self) -> None:
        print("Должность: 1. Пилот  2. Бортпроводник  3. Грузчик  4. Офицер СБ  5. Диспетчер  6. Агент регистрации")
        role = _prompt("Выбор должности", "1")
        fn = _prompt("Имя", "Алексей")
        ln = _prompt("Фамилия", "Громов")
        pass_num = _prompt("Номер паспорта", f"PP{_prompt_int('ID', 505)}")
        sal = _prompt_float("Оклад (BYN)", 3000.0)
        emp = self._create_employee(role, fn, ln, pass_num, sal)
        emp.clock_in()
        self.facade.register_employee(emp)
        print(f"✅ Нанят сотрудник [{type(emp).__name__}] {emp.full_name} ({emp.employee_id}).")

    def _create_employee(self, role: str, fn: str, ln: str, pass_num: str, sal: float) -> Employee:
        if role == "2":
            return FlightAttendant(fn, ln, pass_num, sal, ["Русский", "Английский"])
        if role == "3":
            return BaggageHandler(fn, ln, pass_num, sal)
        if role == "4":
            return SecurityOfficer(fn, ln, pass_num, sal)
        if role == "5":
            return Dispatcher(fn, ln, pass_num, sal, "Main Tower")
        if role == "6":
            return CheckInAgent(fn, ln, pass_num, sal)
        return Pilot(fn, ln, pass_num, sal, "ATPL", is_captain=False)

    def _remove_employee(self) -> None:
        eid = _prompt("Табельный номер сотрудника (например, EMP-BH-202)", "EMP-BH-202")
        emp = next((e for e in self.facade.employees if e.employee_id == eid), None)
        if not emp:
            print("❌ Сотрудник не найден.")
            return
        self.facade.employees.remove(emp)
        print(f"✅ Сотрудник {emp.full_name} ({eid}) уволен.")

    def _add_passenger(self) -> None:
        fn = _prompt("Имя пассажира", "Сергей")
        ln = _prompt("Фамилия", "Ветров")
        pass_num = _prompt("Номер паспорта", "MP998811")
        self.facade.register_passenger(fn, ln, pass_num)
        print(f"✅ Пассажир {fn} {ln} (паспорт {pass_num}) зарегистрирован в системе.")

    def _toggle_duty(self) -> None:
        eid = _prompt("Табельный номер сотрудника", "EMP-PP-101")
        emp = next((e for e in self.facade.employees if e.employee_id == eid), None)
        if not emp:
            print("❌ Сотрудник не найден.")
            return
        if emp.is_on_shift:
            emp.clock_out()
            print(f"✅ Сотрудник {emp.full_name} сдал смену (clock-out).")
        else:
            emp.clock_in()
            print(f"✅ Сотрудник {emp.full_name} заступил на смену (clock-in).")

    def _menu_people(self) -> None:
        while True:
            print("\n--- 👥 ПЕРСОНАЛ И ПАССАЖИРЫ (people/) ---")
            print("1. Список сотрудников и пассажиров\n2. Нанять сотрудника (полиморфизм должностей)")
            print("3. Уволить сотрудника\n4. Добавить (зарегистрировать) пассажира")
            print("5. Смена (clock-in / clock-out)\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_people()
            elif ch == "2":
                self._add_employee()
            elif ch == "3":
                self._remove_employee()
            elif ch == "4":
                self._add_passenger()
            elif ch == "5":
                self._toggle_duty()
            elif ch == "0":
                break

    def _show_schedule(self) -> None:
        print("\n--- 📋 ТАБЛО РЕЙСОВ (Schedule) ---")
        departures = self.facade.schedule.get_departures()
        if not departures:
            print(" Рейсов нет.")
        for f in departures:
            g = f.assigned_gate.number if f.assigned_gate else "TBD"
            print(f" └─ Рейс {f.flight_number} | {f.plan.origin} -> {f.plan.destination} | Статус: {f.status} | Борт: {f.aircraft.tail_number} | Гейт: {g}")

    def _create_flight(self) -> None:
        f_num = _prompt("Номер рейса", "B2-995")
        orig = _prompt("Аэропорт вылета", "MSQ")
        dest = _prompt("Аэропорт назначения", "IST")
        tail = _prompt("Бортовой номер самолета", "EW-737MS")
        dep_time = datetime.now(UTC) + timedelta(hours=3)
        flight = self.facade.create_departure_flight(f_num, "Belavia", tail, orig, dest, dep_time)
        flight.assign_gate(self.state["gate"])
        print(f"✅ Рейс {flight.flight_number} ({orig}->{dest}) внесен в расписание.")

    def _issue_ticket(self) -> None:
        pass_num = _prompt("Номер паспорта", "KH777888")
        f_num = _prompt("Номер рейса", "B2-990")
        price = _prompt_float("Цена билета (USD)", 250.0)
        t = self.facade.issue_ticket(pass_num, f_num, seat_class="Economy", price=price)
        print(f"✅ Оформлен билет #{t.ticket_number} на рейс {f_num} для паспорта {pass_num}.")

    def _check_in(self) -> None:
        pass_num = _prompt("Номер паспорта", "KH777888")
        f_num = _prompt("Номер рейса", "B2-990")
        bag = _prompt_float("Вес багажа в кг (0 если ручная)", 18.5)
        bag_arg = bag if bag > 0 else None
        bp = self.facade.check_in_passenger(pass_num, f_num, baggage_weight=bag_arg)
        print(f"✅ Посадочный талон выдан! Место: {bp.seat_number}, Гейт: {bp.gate_number}.")

    def _cancel_flight(self) -> None:
        f_num = _prompt("Номер рейса для отмены", "B2-995")
        flight = self.facade.find_departure_flight(f_num)
        if not flight:
            print("❌ Рейс не найден.")
            return
        flight.cancel()
        print(f"✅ Рейс {f_num} отменен. Текущий статус: {flight.status}.")

    def _menu_operations(self) -> None:
        while True:
            print("\n--- 🛫 ОПЕРАЦИОННАЯ ДЕЯТЕЛЬНОСТЬ (operations/) ---")
            print("1. Табло рейсов\n2. Создать новый рейс\n3. Оформить билет пассажиру")
            print("4. Регистрация на рейс и сдача багажа\n5. Отменить рейс\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_schedule()
            elif ch == "2":
                self._create_flight()
            elif ch == "3":
                self._issue_ticket()
            elif ch == "4":
                self._check_in()
            elif ch == "5":
                self._cancel_flight()
            elif ch == "0":
                break

    def _scan_passenger_detector(self) -> None:
        detector = MetalDetector("MD-Gate-1")
        p: Passenger = self.state["passr"]
        res = detector.scan(p)
        print(f"🛂 Металлодетектор [{detector.scanner_id}]: Пассажир {p.full_name} -> Результат: {'ТРЕВОГА' if res else 'Чисто'}")

    def _scan_baggage_xray(self) -> None:
        xray = XRayScanner("XRay-Belt-2")
        p: Passenger = self.state["passr"]
        bag = Baggage(19.0, p, "TAG-999")
        res = xray.scan(bag)
        print(f"🧳 Интроскоп [{xray.scanner_id}]: Багаж {bag.tag_number} ({bag.weight_kg} кг) -> Подозрительно: {res}")

    def _check_passport_and_visa(self) -> None:
        control = PassportControl(booth_number=2)
        p: Passenger = self.state["passr"]
        exp = datetime.now(UTC) + timedelta(days=60)
        visa = Visa("UAE", exp)
        control.check_documents(p, visa, "UAE")
        print(f"🛂 Паспортный контроль пройден! Пассажир {p.full_name} допущен в UAE (виза до {exp.date()}).")

    def _check_customs(self) -> None:
        customs = CustomsControl()
        p: Passenger = self.state["passr"]
        val = _prompt_float("Сумма декларируемых ценностей ($)", 4500.0)
        decl = CustomsDeclaration(p, ["Часы", "Электроника"], val)
        customs.inspect_declaration(decl)
        print(f"🛃 Таможня одобрила декларацию #{decl.declaration_id} на сумму {decl.cash_amount} USD.")

    def _menu_security(self) -> None:
        while True:
            print("\n--- 🛡️ СЛУЖБА БЕЗОПАСНОСТИ (security/) ---")
            print("1. Досмотр пассажира через металлодетектор (MetalDetector)")
            print("2. Сканирование багажа рентгеном (XRayScanner)")
            print("3. Проверка паспорта и визы (PassportControl & Visa)")
            print("4. Таможенный контроль (CustomsControl & CustomsDeclaration)\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._scan_passenger_detector()
            elif ch == "2":
                self._scan_baggage_xray()
            elif ch == "3":
                self._check_passport_and_visa()
            elif ch == "4":
                self._check_customs()
            elif ch == "0":
                break

    def _show_weather(self) -> None:
        rep = WeatherReport(temperature_c=18.5, wind_speed_ms=6.2, visibility_m=10000.0, is_stormy=False)
        print("\n🌤️ Метеосводка аэропорта:")
        print(f" └─ Температура: {rep.temperature_c}°C | Ветер: {rep.wind_speed_ms} м/с | Видимость: {rep.visibility_m}м")
        print(f" └─ Условия летные: {rep.is_acceptable_for_takeoff()}")

    def _run_maintenance_task(self) -> None:
        print("Задача ТО: 1. Осмотр (MaintenanceInspection)  2. Заправка (RefuelingTask)")
        print("           3. Клининг салона (CleaningTask)   4. Бортовое питание (CateringTask)")
        ch = _prompt("Выбор", "1")
        plane: Aircraft = self.facade.aircrafts[0]
        handler: BaggageHandler = self.state["handler"]
        truck: FuelTruck = self.state["truck"]
        task = self._build_service_task(ch, plane, truck, handler)
        res = task.execute()
        print(f"✅ Задача [{type(task).__name__}] {task.task_code} выполнена ({res}). Статус: {task.status}.")

    def _build_service_task(self, ch: str, plane: Aircraft, truck: FuelTruck, handler: Employee) -> ServiceTask:
        task: ServiceTask
        if ch == "2":
            task = RefuelingTask(plane, truck, 4000.0, task_code="RF-01")
        elif ch == "3":
            task = CleaningTask(plane, requires_deep_cleaning=False, task_code="CL-01")
        elif ch == "4":
            task = CateringTask(plane, meals_count=150, includes_vip=True, task_code="CT-01")
        else:
            task = MaintenanceInspection(plane, task_code="MI-01", inspector_license="EASA-PART66")
        task.assign_staff(handler)
        return task

    def _menu_maintenance(self) -> None:
        while True:
            print("\n--- 🛠️ НАЗЕМНОЕ ОБСЛУЖИВАНИЕ (maintenance/) ---")
            print("1. Метеосводка (WeatherReport)")
            print("2. Выполнить полиморфную задачу обслуживания (ТО, Заправка, Клининг, Кейтеринг)\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_weather()
            elif ch == "2":
                self._run_maintenance_task()
            elif ch == "0":
                break

    def _run_full_facade_cycle(self) -> None:
        f_num = _prompt("Номер рейса для комплексного цикла", "B2-990")
        fuel = _prompt_float("Объем заправки (литров)", 4000.0)
        print(f"Запуск подготовки рейса {f_num} через Фасад...")
        self.facade.prepare_flight(f_num, fuel_amount=fuel)
        print("✅ Техническое обслуживание пройдено, борт заправлен.")
        runway = self.facade.dispatch_takeoff(f_num)
        print(f"🛫 ВЗЛЕТ РАЗРЕШЕН! Рейс {f_num} успешно покинул ВПП {runway.number}.")

    def _menu_facade(self) -> None:
        while True:
            print("\n--- 🎮 ФАСАД АЭРОПОРТА (facade/) ---")
            print("1. Запустить полный цикл вылета рейса (подготовка, заправка, взлет)\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._run_full_facade_cycle()
            elif ch == "0":
                break

    def _handle_menu_choice(self, choice: str) -> None:
        actions: dict[str, Callable[[], object]] = {
            "1": self._menu_fleet,
            "2": self._menu_infrastructure,
            "3": self._menu_people,
            "4": self._menu_operations,
            "5": self._menu_security,
            "6": self._menu_maintenance,
            "7": self._menu_facade,
            "8": self.save_state,
            "9": self.load_state,
        }
        if choice in actions:
            actions[choice]()
        elif choice == "0":
            print("🚪 Завершение работы системы аэропорта. До свидания!")
            sys.exit(0)
        else:
            print("⚠️ Неизвестная команда.")

    def _print_main_menu(self) -> None:
        print("\n" + "=" * 60)
        print("✈️  СИСТЕМА УПРАВЛЕНИЯ АЭРОПОРТОМ (LAB 3 INTERACTIVE)")
        print("=" * 60)
        print("1. 🛫 Флот и перрон (fleet/: самолеты, спецтехника, действия)")
        print("2. 🏢 Инфраструктура (infrastructure/: терминалы, ВПП, ангар, парковка)")
        print("3. 👥 Персонал (people/: экипажи, наземные службы, пассажиры)")
        print("4. 📋 Операции и полеты (operations/: рейсы, билеты, посадка)")
        print("5. 🛡️  Безопасность (security/: детекторы, рентген, паспорт, таможня)")
        print("6. 🛠️  Техобслуживание (maintenance/: ТО, заправка, клининг, погода)")
        print("7. 🎮 Фасад вылета (facade/: комплексный цикл взлета)")
        print("8. 💾 Сохранить состояние в файл (Pickle State)")
        print("9. 📂 Загрузить состояние из файла (Pickle State)")
        print("0. Выход\n" + "=" * 60)

    def run(self) -> None:
        while True:
            self._print_main_menu()
            choice = input("\nВыбор > ").strip()
            try:
                self._handle_menu_choice(choice)
            except AirportException as e:
                print(f"\n❌ БИЗНЕС-ОШИБКА АЭРОПОРТА: {e}")
            except ValueError as e:
                print(f"\n⚠️ ОШИБКА ДАННЫХ: {e}")
            except Exception as e:  # noqa: BLE001
                print(f"\n🔥 КРИТИЧЕСКАЯ ОШИБКА: {e}")


def main() -> None:
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
