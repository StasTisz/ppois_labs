"""Консольный интерфейс (CLI) для демонстрации работы системы Аэропорта (Лаба №3).

Покрывает все подсистемы и полиморфные иерархии:
- fleet/ (самолеты и перронная спецтехника)
- infrastructure/ (терминал, ВПП, гейты, ангар, карусель, зал)
- people/ (пилоты, бортпроводники, грузчики, инспекторы безопасности)
- operations/ (рейсы, билеты, посадочные, расписание)
- security/ (рамки металлодетектора, рентген-сканеры, визы, таможня)
- maintenance/ (регламентные задачи ТО, клининг, заправка, метеосводки)
- facade/ (сквозной координатор бизнес-процессов)
"""

from __future__ import annotations

import os
import pickle
import sys
from datetime import UTC, datetime, timedelta

from lab3.domain.exceptions import AirportException
from lab3.domain.facade import AirportFacade
from lab3.domain.fleet import (
    BaggageTractor,
    CargoAircraft,
    FollowMeCar,
    FuelTruck,
    PassengerAircraft,
    PassengerBus,
    PrivateJet,
)
from lab3.domain.infrastructure import (
    BaggageCarousel,
    CheckInCounter,
    Gate,
    Hangar,
    Lounge,
    ParkingLot,
    Runway,
    Terminal,
)
from lab3.domain.maintenance import (
    CateringTask,
    CleaningTask,
    MaintenanceInspection,
    RefuelingTask,
    WeatherReport,
)
from lab3.domain.operations import (
    ArrivalFlight,
    Baggage,
    BoardingPass,
    DepartureFlight,
    FlightPlan,
    Ticket,
)
from lab3.domain.people import (
    BaggageHandler,
    CheckInAgent,
    Dispatcher,
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
    SecurityCheckpoint,
    Visa,
    XRayScanner,
)

DEFAULT_STATE_FILE = "airport_state.pkl"


class AirportDataSeeder:
    """Генератор масштабной доменной модели аэропорта со всеми сущностями."""

    @staticmethod
    def _seed_fleet() -> tuple[
        PassengerAircraft, CargoAircraft, PrivateJet,
        PassengerBus, BaggageTractor, FuelTruck, FollowMeCar,
    ]:
        plane = PassengerAircraft("Boeing 737-800", 850.0, "EW-001", 18000.0, 150)
        cargo = CargoAircraft("Ил-76ТД", 750.0, "EW-760", 42000.0, 35000.0)
        jet = PrivateJet("Gulfstream G650", 950.0, "EW-007", 9000.0, "VIP Aviation")
        bus = PassengerBus("МАЗ-171", 45.0, "BUS-01", 100)
        tractor = BaggageTractor("БелАЗ-Тягач", 25.0, "TR-01", 4)
        truck = FuelTruck("Volvo-Refueler", 60.0, "FT-01", 25000.0)
        follow = FollowMeCar("Geely-Leader", 120.0, "FM-01")
        return plane, cargo, jet, bus, tractor, truck, follow

    @staticmethod
    def _seed_staff() -> tuple[
        Pilot, FlightAttendant, BaggageHandler, SecurityOfficer, Dispatcher, CheckInAgent,
    ]:
        pilot = Pilot("Иван", "Иванов", "PP-101", 5200.0, "ATPL", is_captain=True)
        attendant = FlightAttendant("Ольга", "Петрова", "PP-202", 2600.0)
        handler = BaggageHandler("Сергей", "Сидоров", "PP-303", 1900.0)
        officer = SecurityOfficer("Анна", "Смирнова", "PP-404", 2100.0)
        dispatcher = Dispatcher("Михаил", "Козлов", "PP-505", 3100.0)
        agent = CheckInAgent("Елена", "Васильева", "PP-606", 2300.0)
        for emp in (pilot, attendant, handler, officer, dispatcher, agent):
            emp.clock_in()
        return pilot, attendant, handler, officer, dispatcher, agent

    @staticmethod
    def _seed_infra(facade: AirportFacade) -> tuple[
        Terminal, Gate, Runway, Hangar, BaggageCarousel, CheckInCounter, Lounge, ParkingLot,
    ]:
        term = Terminal("Терминал 1")
        gate_a1 = Gate("A1")
        term.add_gate(gate_a1)
        carousel = BaggageCarousel(1)
        term.add_carousel(carousel)
        counter = CheckInCounter(1)
        term.add_counter(counter)
        lounge = Lounge("VIP Lounge Belavia", capacity=40, is_vip=True)
        term.add_lounge(lounge)
        facade.airport.add_terminal(term)
        runway = Runway("01L", 3500)
        facade.airport.control_tower.add_runway(runway)
        hangar = Hangar(1, capacity=3)
        parking = ParkingLot("P1", total_spaces=150)
        return term, gate_a1, runway, hangar, carousel, counter, lounge, parking

    @staticmethod
    def seed(facade: AirportFacade) -> dict:
        plane, cargo, jet, bus, tractor, truck, follow = AirportDataSeeder._seed_fleet()
        pilot, att, handler, officer, disp, agent = AirportDataSeeder._seed_staff()
        term, gate_a1, rwy, hng, car, cnt, lng, prk = AirportDataSeeder._seed_infra(facade)
        facade.register_aircraft(plane)
        facade.register_fuel_truck(truck)
        facade.register_employee(pilot)
        facade.checkpoint.assign_officer(officer)
        passenger = Passenger("Стас", "Разработчиков", "MP-1234567")
        facade.register_passenger(passenger.first_name, passenger.last_name, passenger.passport_number)
        dep_flight = facade.create_departure_flight(
            "B2-100", "Belavia", "EW-001", "MSQ", "SVO", datetime.now() + timedelta(hours=2)
        )
        dep_flight.assign_gate(gate_a1)
        passenger = Passenger("Стас", "Разработчиков", "MP-1234567")
        return {
            "plane": plane, "cargo": cargo, "jet": jet,
            "bus": bus, "tractor": tractor, "truck": truck, "follow": follow,
            "pilot": pilot, "attendant": att, "handler": handler,
            "officer": officer, "dispatcher": disp, "agent": agent,
            "terminal": term, "gate": gate_a1, "runway": rwy,
            "hangar": hng, "carousel": car, "counter": cnt,
            "lounge": lng, "parking": prk, "dep_flight": dep_flight,
            "passenger": passenger,
        }


class AirportCLI:
    """Консольный интерфейс системы управления Международным Аэропортом (Лаба №3)."""

    def __init__(self, state_file: str = DEFAULT_STATE_FILE) -> None:
        self.state_file = state_file
        print(">>> Инициализация доменной модели Аэропорта (MSQ)...")
        self.facade = AirportFacade("Национальный аэропорт Минск", "MSQ")
        self.state = AirportDataSeeder.seed(self.facade)
        print(">>> Все службы и полиморфные подсистемы готовы к работе.\n")

    def save(self) -> None:
        with open(self.state_file, "wb") as f:
            pickle.dump((self.facade, self.state), f)
        print(f"💾 Полное состояние аэропорта сохранено в '{self.state_file}'.")

    def load(self) -> None:
        if not os.path.exists(self.state_file):
            print(f"⚠️ Файл '{self.state_file}' не найден.")
            return
        with open(self.state_file, "rb") as f:
            self.facade, self.state = pickle.load(f)
        print(f"📂 Состояние аэропорта успешно восстановлено из '{self.state_file}'.")

    def run(self) -> None:
        menu_map = {
            "1": self._menu_fleet,
            "2": self._menu_infrastructure,
            "3": self._menu_people,
            "4": self._menu_operations,
            "5": self._menu_security,
            "6": self._menu_maintenance,
            "7": self._menu_facade,
            "8": self.save,
            "9": self.load,
        }
        while True:
            self._print_main_menu()
            choice = input("\nВыберите раздел (0-9): ").strip()
            if choice == "0":
                print("🚪 Завершение работы системы Аэропорта. До свидания!")
                sys.exit(0)
            if choice in menu_map:
                try:
                    menu_map[choice]()
                except AirportException as e:
                    print(f"\n❌ ОШИБКА АВИАЦИОННОЙ ЛОГИКИ: {e}")
                except Exception as e:  # noqa: BLE001
                    print(f"\n🔥 СБОЙ ОПЕРАЦИИ: {e}")
            else:
                print("⚠️ Неизвестная команда.")

    def _print_main_menu(self) -> None:
        print("\n" + "=" * 65)
        print(" ✈️   АЭРОПОРТ МИНСК - УПРАВЛЕНИЕ АВИАУЗЛОМ (LAB 3 ENTERPRISE)")
        print("=" * 65)
        print("1. 🛫 Авиапарк и Перрон (fleet/: полиморфизм самолетов и техники)")
        print("2. 🏛️ Инфраструктура (infrastructure/: ВПП, гейты, ангар, карусель)")
        print("3. 👥 Персонал и Экипажи (people/: пилот, стюардесса, грузчик, офицер)")
        print("4. 📋 Полетные операции (operations/: рейсы, билеты, багаж)")
        print("5. 🛡️ Авиационная безопасность (security/: рамки, рентген, визы)")
        print("6. 🔧 Наземное ТО (maintenance/: регламентные задачи, погода METAR)")
        print("7. 🚀 Сквозной бизнес-процесс (facade/: комплексный цикл вылета)")
        print("8. 💾 Сохранить состояние системы (pickle)")
        print("9. 📂 Загрузить состояние системы (pickle)")
        print("0. Выход\n" + "=" * 65)

    # ---------------- 1. АВИАПАРК (fleet/) ----------------
    def _demo_aircraft_polymorphism(self) -> None:
        plane: PassengerAircraft = self.state["plane"]
        cargo: CargoAircraft = self.state["cargo"]
        jet: PrivateJet = self.state["jet"]
        print("\n[Полиморфизм воздушных судов (Aircraft)]:")
        plane.board_passengers(142)
        print(f" -> Пассажирский {plane.model} ({plane.tail_number}): на борту {plane.passengers_count} пасс.")
        cargo.load_cargo(28500.0)
        print(f" -> Грузовой {cargo.model} ({cargo.tail_number}): карго {cargo.current_payload_kg}/{cargo.max_payload_kg} кг.")
        jet.order_vip_catering()
        print(f" -> Бизнес-джет {jet.model} ({jet.tail_number}): владелец '{jet.owner_name}', кейтеринг={jet.is_vip_catered}")

    def _demo_ground_vehicles(self) -> None:
        bus: PassengerBus = self.state["bus"]
        tractor: BaggageTractor = self.state["tractor"]
        truck: FuelTruck = self.state["truck"]
        follow: FollowMeCar = self.state["follow"]
        p: Passenger = self.state["passenger"]
        plane: PassengerAircraft = self.state["plane"]
        print("\n[Полиморфизм перронной техники (GroundVehicle)]:")
        bus.board_passenger(p)
        print(f" -> Автобус {bus.model}: посажен пассажир {p.full_name}")
        tractor.attach_cart()
        bag = Baggage(21.0, p, "BG-TR-01")
        tractor.transport_baggage(bag)
        print(f" -> Тягач {tractor.model}: доставка багажа к борту (прицепов: {tractor.current_carts})")
        truck.refuel_aircraft(plane, 3500.0)
        print(f" -> Топливозаправщик {truck.model}: заправлено 3500 л (в баках борта {plane.current_fuel} л)")
        follow.toggle_lights()
        follow.lead_aircraft(plane, "Стоянка 12")
        print(f" -> Машина сопровождения {follow.model}: борт лидирован на стоянку")

    def _menu_fleet(self) -> None:
        print("\n--- 🛫 АВИАПАРК И ПЕРРОННАЯ ТЕХНИКА (fleet/) ---")
        self._demo_aircraft_polymorphism()
        self._demo_ground_vehicles()

    # ---------------- 2. ИНФРАСТРУКТУРА (infrastructure/) ----------------
    def _demo_runway_and_tower(self) -> None:
        tower = self.facade.airport.control_tower
        rwy: Runway = self.state["runway"]
        plane: PassengerAircraft = self.state["plane"]
        print(f"1. Вышка УВД '{tower.tower_name}':")
        assigned_rwy = tower.request_takeoff(plane)
        print(f" └─ Диспетчер выделил ВПП: {assigned_rwy.number} (длина: {assigned_rwy.length} м)")
        rwy.clear()

    def _demo_terminal_facilities(self) -> None:
        gate: Gate = self.state["gate"]
        hng: Hangar = self.state["hangar"]
        car: BaggageCarousel = self.state["carousel"]
        lng: Lounge = self.state["lounge"]
        prk: ParkingLot = self.state["parking"]
        cargo: CargoAircraft = self.state["cargo"]
        follow: FollowMeCar = self.state["follow"]
        print(f"2. Гейт {gate.number}: открыт={gate.is_open}, привязан рейс={gate.current_flight is not None}")
        hng.store_aircraft(cargo)
        print(f"3. Ангар #{hng.number}: борт {cargo.model} на регламенте (в ангаре: {len(hng.stored_aircraft)}/{hng.capacity})")
        hng.release_aircraft(cargo)
        car.activate()
        print(f"4. Багажная лента #{car.number}: статус транспортера = {car.is_active}")
        car.deactivate()
        p: Passenger = self.state["passenger"]
        lng.enter(p)
        print(f"5. Бизнес-зал '{lng.name}': гостей {lng.current_occupancy}/{lng.capacity}")
        lng.exit(p)
        prk.park_car(follow)
        print(f"6. Парковка '{prk.zone_code}': свободных мест = {prk.available_spaces}/{prk.total_spaces}")

    def _menu_infrastructure(self) -> None:
        print("\n--- 🏛️ ИНФРАСТРУКТУРА АЭРОПОРТА (infrastructure/) ---")
        self._demo_runway_and_tower()
        self._demo_terminal_facilities()

    # ---------------- 3. ПЕРСОНАЛ (people/) ----------------
    def _demo_cockpit_cabin_crew(self) -> None:
        pilot: Pilot = self.state["pilot"]
        att: FlightAttendant = self.state["attendant"]
        dep: DepartureFlight = self.state["dep_flight"]
        print("[Летный состав]:")
        pilot.conduct_preflight_briefing(dep.plan)
        pilot.log_flight_hours(3)
        print(f" -> КВС {pilot.full_name}: предполетный брифинг проведен, налет {pilot.flight_hours} ч.")
        att.demonstrate_safety_equipment()
        att.serve_passengers(120)
        print(f" -> Бортпроводник {att.full_name}: инструктаж показан, 120 рационов роздано")

    def _demo_ground_staff(self) -> None:
        handler: BaggageHandler = self.state["handler"]
        officer: SecurityOfficer = self.state["officer"]
        disp: Dispatcher = self.state["dispatcher"]
        agent: CheckInAgent = self.state["agent"]
        p: Passenger = self.state["passenger"]
        dep: DepartureFlight = self.state["dep_flight"]
        bag = Baggage(18.5, p, "BG-001")
        print("\n[Наземные службы]:")
        handler.load_to_cargo_hold(dep, bag)
        print(f" -> Грузчик {handler.full_name}: погрузил сумку {bag.tag_number} в багажный отсек рейса")
        disp.issue_weather_alert("Боковой ветер 12 м/с на ВПП 01L")
        print(f" -> Диспетчер {disp.full_name}: метео-оповещение выпущено")
        agent.tag_baggage(bag)
        print(f" -> Агент регистрации {agent.full_name}: багаж зарегистрирован")
        print(f" -> Инспектор безопасности {officer.full_name}: дежурство = {officer.is_on_shift}")

    def _menu_people(self) -> None:
        print("\n--- 👥 ПЕРСОНАЛ И ЭКИПАЖИ (people/) ---")
        self._demo_cockpit_cabin_crew()
        self._demo_ground_staff()

    # ---------------- 4. ОПЕРАЦИИ (operations/) ----------------
    def _menu_operations(self) -> None:
        print("\n--- 📋 ПОЛЕТНЫЕ ОПЕРАЦИИ (operations/) ---")
        dep: DepartureFlight = self.state["dep_flight"]
        p: Passenger = self.state["passenger"]
        plan: FlightPlan = dep.plan
        gate: Gate = self.state["gate"]
        print(f"1. План полета {dep.flight_number}: {plan.origin} -> {plan.destination}")
        print(f" └─ Международный: {plan.is_international()} | Расчетное время: {plan.calculate_flight_duration_hours():.1f} ч.")
        ticket = Ticket(p, dep, "Economy", 180.0, "TK-888999")
        ticket.upgrade_class("Business")
        print(f"2. Электронный билет #{ticket.ticket_number}: класс повышен до '{ticket.seat_class}'")
        bp = BoardingPass(ticket, "02B", gate)
        bp.change_seat("01A")
        bp.mark_boarded()
        print(f"3. Посадочный талон: кресло {bp.seat_number}, гейт {bp.gate_number}, посажен={bp.is_boarded}")
        bag = Baggage(16.0, p, "BG-VIP")
        bag.attach_tag("RUSH-PRIORITY")
        bag.check_weight()
        print(f"4. Багаж: {bag.tag_number} (вес: {bag.weight_kg} кг, проверен: {bag.is_inspected})")
        arr = ArrivalFlight("SU-1830", dep.airline, dep.aircraft, FlightPlan("SVO", "MSQ", datetime.now()))
        print(f"5. Входящий рейс: {arr.flight_number} ({arr.plan.origin} -> {arr.plan.destination})")

    # ---------------- 5. БЕЗОПАСНОСТЬ (security/) ----------------
    def _menu_security(self) -> None:
        print("\n--- 🛡️ АВИАЦИОННАЯ БЕЗОПАСНОСТЬ (security/) ---")
        p: Passenger = self.state["passenger"]
        detector = MetalDetector("Ceia-01", sensitivity_level=4)
        detector.calibrate()
        print(f"1. Стационарный металлодетектор: {detector.model} откалиброван, тест={detector.test_alarm()}")
        detector.scan(p)
        print(f" └─ Пассажир {p.full_name} прошел через рамку чисто")
        xray = XRayScanner("Heimann-XR", contrast_level=1.2)
        bag = Baggage(12.0, p, "BG-SEC")
        xray.scan(bag)
        print(f"2. Интроскоп багажа: рентген-досмотр чемодана {bag.tag_number} завершен")
        checkpoint = SecurityCheckpoint(1)
        checkpoint.assign_equipment(detector, xray)
        checkpoint.assign_officer(self.state["officer"])
        checkpoint.open_checkpoint()
        checkpoint.process_passenger(p, bag)
        print(" └─ Досмотровый пункт: пассажир и ручная кладь допущены в чистую зону")
        self._demo_border_customs(p)

    def _demo_border_customs(self, p: Passenger) -> None:
        passport_ctrl = PassportControl(booth_number=2)
        visa = Visa("UAE", datetime.now(UTC) + timedelta(days=90))
        passport_ctrl.check_documents(p, visa, "UAE")
        passport_ctrl.stamp_entry(p)
        print(f"3. Паспортный контроль: виза {visa.country} проверена, въездной штамп проставлен")
        customs = CustomsControl(control_number=1)
        decl = CustomsDeclaration(p, ["MacBook Pro", "Часы"], 4500.0)
        customs.inspect_declaration(decl)
        customs.stamp_passport(p)
        print("4. Таможенный контроль: декларация проверена, лимиты в норме")

    # ---------------- 6. ТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ (maintenance/) ----------------
    def _menu_maintenance(self) -> None:
        print("\n--- 🔧 НАЗЕМНОЕ ОБСЛУЖИВАНИЕ И METAR (maintenance/) ---")
        plane: PassengerAircraft = self.state["plane"]
        truck: FuelTruck = self.state["truck"]
        handler: BaggageHandler = self.state["handler"]
        task_insp = MaintenanceInspection(plane, "MI-01", inspector_license="EASA-PART66")
        task_refuel = RefuelingTask(plane, truck, 4000.0, "RF-01")
        task_clean = CleaningTask(plane, requires_deep_cleaning=True, task_code="CL-01")
        task_cater = CateringTask(plane, meals_count=150, includes_vip=True, task_code="CT-01")
        tasks = [task_insp, task_refuel, task_clean, task_cater]
        print("Полиморфные задачи наземного обслуживания (ServiceTask):")
        for t in tasks:
            t.assign_staff(handler)
            est_time = t.calculate_estimated_duration_minutes()
            print(f" └─ Задача [{t.task_code}]: расчетная длительность = {est_time} мин.")
            res = t.execute()
            print(f"    ├─ Результат выполнения: {res}")
        print(" -> Все регламентные задачи выполнены инженерной бригадой")
        metar = WeatherReport(temperature_c=17.5, wind_speed_ms=6.0, visibility_m=10000.0, is_stormy=False)
        print(f"\nМетеосводка: {metar.format_metar()}")
        print(f"Допуск метеоусловий к выполнению взлета: {metar.is_acceptable_for_takeoff()}")

    # ---------------- 7. СКВОЗНОЙ СЦЕНАРИЙ (facade/) ----------------
    def _menu_facade(self) -> None:
        print("\n--- 🚀 СКВОЗНОЙ СЦЕНАРИЙ ОБСЛУЖИВАНИЯ РЕЙСА (facade/) ---")
        p: Passenger = self.state["passenger"]
        flight_num = "B2-100"
        print("1. Оформление электронного билета через фасад...")
        ticket = self.facade.issue_ticket(p.passport_number, flight_num, "Economy", 160.0)
        print(f" └─ Билет #{ticket.ticket_number} выписан на рейс {flight_num}")
        print("2. Регистрация на стойке и сдача багажа...")
        bp = self.facade.check_in_passenger(p.passport_number, flight_num, baggage_weight=19.5)
        print(f" └─ Посадочный талон: кресло {bp.seat_number}, гейт {bp.gate_number}")
        print("3. Комплексная предполетная подготовка воздушного судна...")
        self.facade.prepare_flight(flight_num, fuel_amount=4200.0)
        print(" └─ Техосмотр пройден, заправка завершена")
        print("4. Запрос диспетчерской вышке на вылет...")
        rwy = self.facade.dispatch_takeoff(flight_num)
        print(f" 🛫 ВЗЛЕТ РАЗРЕШЕН! Рейс {flight_num} произвел взлет с ВПП {rwy.number}!")


if __name__ == "__main__":
    app = AirportCLI()
    app.run()
