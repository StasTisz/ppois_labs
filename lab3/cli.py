"""
Консольный интерфейс (CLI) для демонстрации работы системы Аэропорта.
Охватывает основные модули: инфраструктуру, флот, операции, людей и безопасность.
"""

import sys
from datetime import datetime, timedelta

# Импортируем базовое исключение и фасад
from lab3.domain.exceptions import AirportException
from lab3.domain.facade import AirportFacade

# Импорты для Data Seeder и демонстрации работы отдельных модулей
from lab3.domain.fleet import PassengerAircraft, FuelTruck
from lab3.domain.infrastructure import Runway, Terminal, Gate
from lab3.domain.people import Pilot, SecurityOfficer, Passenger
from lab3.domain.security import CustomsControl, CustomsDeclaration, PassportControl, Visa


def seed_initial_data(facade: AirportFacade) -> None:
    """Генерирует начальные данные (инфраструктуру, флот, рейсы) для демонстрации."""
    print(">>> Инициализация систем аэропорта...")

    # 1. Инфраструктура
    facade.airport.control_tower.add_runway(Runway("01L", 3500))
    facade.airport.control_tower.add_runway(Runway("01R", 3000))

    terminal = Terminal("Terminal 1")
    gate_a1 = Gate("A1")
    terminal.add_gate(gate_a1)
    facade.airport.add_terminal(terminal)

    # 2. Флот
    plane = PassengerAircraft("Boeing 737", 850.0, "EW-001", 15000.0, 150)
    # Имитируем, что самолет только что прилетел и требует ТО
    plane.requires_maintenance = True
    facade.register_aircraft(plane)

    truck = FuelTruck("Volvo", 60.0, "FT-01", 20000.0)
    facade.register_fuel_truck(truck)

    # 3. Персонал
    pilot = Pilot("Иван", "Иванов", "PP-111", 5000.0, "ATPL", is_captain=True)
    pilot.clock_in()
    facade.register_employee(pilot)

    security = SecurityOfficer("Анна", "Смирнова", "PP-999", 2000.0)
    security.clock_in()
    facade.checkpoint.assign_officer(security)

    # 4. Формирование тестового рейса
    flight = facade.create_departure_flight(
        flight_number="B2-100",
        airline_name="Belavia",
        tail_number="EW-001",
        origin="MSQ",
        destination="SVO",
        scheduled_time=datetime.now() + timedelta(hours=2)
    )
    flight.assign_gate(gate_a1)
    print(">>> Аэропорт готов к работе. Тестовый рейс B2-100 создан.\n")


def print_menu() -> None:
    """Выводит главное меню в консоль."""
    print("\n" + "=" * 45)
    print(" ✈️   АЭРОПОРТ МИНСК - ПАНЕЛЬ УПРАВЛЕНИЯ ")
    print("=" * 45)
    print("1. Табло рейсов (Расписание)")
    print("2. Продажа билета (Регистрация нового пассажира)")
    print("3. Стойка регистрации и сдача багажа")
    print("4. Наземное обслуживание (ТО и заправка борта)")
    print("5. Диспетчерская вышка (Запрос на взлет)")
    print("6. Демонстрация модуля безопасности (Таможня/Визы)")
    print("0. Выход из системы")
    print("=" * 45)


def handle_show_schedule(facade: AirportFacade) -> None:
    print("\n--- ТАБЛО ВЫЛЕТОВ ---")
    departures = facade.schedule.get_departures()
    if not departures:
        print("Нет запланированных рейсов.")
    for f in departures:
        gate_num = f.assigned_gate.number if f.assigned_gate else "TBD"
        print(f"Рейс: {f.flight_number} | {f.plan.origin} -> {f.plan.destination} | "
              f"Статус: {f.status} | Борт: {f.aircraft.tail_number} | Гейт: {gate_num}")


def handle_buy_ticket(facade: AirportFacade) -> None:
    print("\n--- ОФОРМЛЕНИЕ БИЛЕТА ---")
    first_name = input("Имя пассажира: ").strip()
    last_name = input("Фамилия пассажира: ").strip()
    passport = input("Номер паспорта: ").strip()

    facade.register_passenger(first_name, last_name, passport)
    flight_num = input("Номер рейса (например, B2-100): ").strip()

    try:
        ticket = facade.issue_ticket(passport, flight_num, "Economy", 150.0)
        print(f"✅ Успешно! Билет #{ticket.ticket_number} оформлен на пассажира {first_name} {last_name}.")
    except AirportException as e:
        print(f"❌ Ошибка доменной логики: {e}")
    except ValueError as e:
        print(f"❌ Ошибка данных: {e}")


def handle_check_in(facade: AirportFacade) -> None:
    print("\n--- СТОЙКА РЕГИСТРАЦИИ (CHECK-IN) ---")
    passport = input("Введите номер паспорта: ").strip()
    flight_num = input("Введите номер рейса (например, B2-100): ").strip()

    bag_input = input("Вес багажа в кг (оставьте пустым, если без багажа): ").strip()
    baggage_weight = float(bag_input) if bag_input else None

    try:
        boarding_pass = facade.check_in_passenger(passport, flight_num, baggage_weight)
        print("\n🎟️  ПОСАДОЧНЫЙ ТАЛОН СГЕНЕРИРОВАН:")
        print(f"    Рейс: {boarding_pass.ticket.flight_number}")
        print(f"    Билет: {boarding_pass.ticket.ticket_number}")
        print(f"    Место в салоне: {boarding_pass.seat_number}")
        print(f"    Гейт для посадки: {boarding_pass.gate_number}")
        if baggage_weight:
            print(f"    💼 Багаж ({baggage_weight} кг) успешно принят в грузовой отсек.")
    except AirportException as e:
        print(f"❌ Отказ в регистрации: {e}")
    except ValueError as e:
        print(f"❌ Системная ошибка: {e}")


def handle_maintenance(facade: AirportFacade) -> None:
    print("\n--- НАЗЕМНОЕ ОБСЛУЖИВАНИЕ ---")
    flight_num = input("Введите номер рейса для обслуживания (например, B2-100): ").strip()
    try:
        print(f"Запуск бригады техников для рейса {flight_num}...")
        facade.prepare_flight(flight_num, fuel_amount=4000.0)
        print("✅ Технический осмотр (Line Maintenance) пройден.")
        print("✅ Борт успешно дозаправлен. Самолет готов к вылету.")
    except AirportException as e:
        print(f"❌ Ошибка обслуживания: {e}")
    except ValueError as e:
        print(f"❌ Ошибка данных: {e}")


def handle_dispatch_takeoff(facade: AirportFacade) -> None:
    print("\n--- ДИСПЕТЧЕРСКАЯ ВЫШКА ---")
    flight_num = input("Введите номер рейса для запроса взлета (например, B2-100): ").strip()
    try:
        runway = facade.dispatch_takeoff(flight_num)
        print(f"🛫 ВЗЛЕТ РАЗРЕШЕН! Рейс {flight_num} успешно покинул ВПП {runway.number}.")
    except AirportException as e:
        print(f"❌ Взлет запрещен: {e}")
    except ValueError as e:
        print(f"❌ Системная ошибка: {e}")


def handle_security_demo() -> None:
    print("\n--- ПОГРАНИЧНЫЙ И ТАМОЖЕННЫЙ КОНТРОЛЬ ---")
    print("Демонстрация работы модулей службы безопасности напрямую (без фасада):")

    test_passenger = Passenger("Джеймс", "Бонд", "007")

    # 1. Пограничный контроль
    border_control = PassportControl(booth_number=3)
    valid_visa = Visa("UK", datetime.now() + timedelta(days=30))
    expired_visa = Visa("UK", datetime.now() - timedelta(days=5))

    print("\n[Проверка действительной визы]")
    try:
        border_control.check_documents(test_passenger, valid_visa, "UK")
        print("✅ Граница пройдена успешно.")
    except AirportException as e:
        print(f"❌ {e}")

    print("\n[Проверка просроченной визы]")
    try:
        border_control.check_documents(test_passenger, expired_visa, "UK")
    except AirportException as e:
        print(f"❌ Нарушение визового режима поймано: {e}")

    # 2. Таможня
    customs = CustomsControl()
    legal_decl = CustomsDeclaration(test_passenger.person_id, ["Часы"], 8000.0)
    illegal_decl = CustomsDeclaration(test_passenger.person_id, ["Золото"], 15000.0)

    print("\n[Проверка таможенной декларации (8000$)]")
    try:
        customs.inspect_declaration(legal_decl)
        print("✅ Таможня дает добро.")
    except AirportException as e:
        print(f"❌ {e}")

    print("\n[Проверка декларации с превышением лимита (15000$)]")
    try:
        customs.inspect_declaration(illegal_decl)
    except AirportException as e:
        print(f"❌ Контрабанда пресечена: {e}")


def main():
    facade = AirportFacade("Minsk National Airport", "MSQ")
    seed_initial_data(facade)

    while True:
        print_menu()
        choice = input("Выберите действие (0-6): ").strip()

        if choice == '1':
            handle_show_schedule(facade)
        elif choice == '2':
            handle_buy_ticket(facade)
        elif choice == '3':
            handle_check_in(facade)
        elif choice == '4':
            handle_maintenance(facade)
        elif choice == '5':
            handle_dispatch_takeoff(facade)
        elif choice == '6':
            handle_security_demo()
        elif choice == '0':
            print("Завершение работы системы аэропорта. До свидания!")
            sys.exit(0)
        else:
            print("❌ Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nАварийный выход из системы.")
        sys.exit(0)