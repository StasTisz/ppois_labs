# Лабораторная работа №3. Объектно-ориентированная архитектура аэропорта

Информационная система крупного аэропорта. Система управляет инфраструктурой (взлетно-посадочные полосы, терминалы, гейты), воздушным и наземным флотом (пассажирские лайнеры, грузовые борта, заправщики, багажные тягачи), контингентом пассажиров и персонала, операционной деятельностью (расписание рейсов, билеты, посадочные талоны, багаж), службой безопасности (рамки, сканеры, визовый и таможенный контроль) и наземным обслуживанием (регламентное ТО, заправка, метеоусловия).

---

## 1. Спецификация классов объектной модели

*Примечание: в столбце «Поля» для дочерних классов учитываются атрибуты, унаследованные от базовых.*

| Класс | Поля | Методы | Ассоциации (связанные классы) |
|---|:---:|:---:|---|
| **Runway** | 5 | 2 | Aircraft |
| **Gate** | 4 | 4 | Flight |
| **CheckInCounter** | 6 | 3 | CheckInAgent, Flight, Baggage |
| **BaggageCarousel** | 4 | 2 | Flight |
| **Lounge** | 5 | 3 | Passenger |
| **Terminal** | 6 | 5 | Gate, CheckInCounter, BaggageCarousel, Lounge |
| **ControlTower** | 3 | 4 | Runway, Aircraft |
| **Hangar** | 4 | 2 | Aircraft |
| **ParkingLot** | 4 | 2 | — |
| **Airport** | 6 | 2 | ControlTower, Terminal, Hangar, ParkingLot |
| **Vehicle** | 5 | 1 | — |
| **Aircraft** | 9 | 5 | — |
| **PassengerAircraft** | 13 | 8 | — |
| **CargoAircraft** | 13 | 8 | — |
| **PrivateJet** | 12 | 6 | — |
| **GroundVehicle** | 7 | 3 | — |
| **BaggageTractor** | 10 | 6 | — |
| **FuelTruck** | 11 | 5 | Aircraft |
| **FollowMeCar** | 8 | 4 | Aircraft |
| **PassengerBus** | 10 | 6 | — |
| **Person** | 4 | 1 | — |
| **Passenger** | 7 | 6 | Ticket, Baggage |
| **Employee** | 7 | 4 | — |
| **CrewMember** | 9 | 6 | — |
| **Pilot** | 12 | 6 | — |
| **FlightAttendant** | 11 | 6 | — |
| **Dispatcher** | 9 | 4 | — |
| **SecurityOfficer** | 7 | 4 | — |
| **CheckInAgent** | 9 | 5 | — |
| **BaggageHandler** | 9 | 5 | — |
| **Baggage** | 4 | 1 | — |
| **Ticket** | 6 | 1 | — |
| **BoardingPass** | 4 | 0 | Ticket |
| **Airline** | 4 | 3 | Aircraft |
| **FlightPlan** | 5 | 0 | — |
| **Flight** | 7 | 2 | Airline, Aircraft, FlightPlan |
| **DepartureFlight** | 11 | 8 | Gate, Passenger, Baggage, Ticket, BoardingPass |
| **ArrivalFlight** | 8 | 4 | BaggageCarousel |
| **Schedule** | 1 | 3 | Flight, DepartureFlight, ArrivalFlight |
| **Visa** | 3 | 1 | — |
| **CustomsDeclaration** | 5 | 2 | — |
| **Scanner** | 3 | 1 | Passenger, Baggage |
| **MetalDetector** | 3 | 1 | Passenger, Baggage |
| **XRayScanner** | 3 | 1 | Passenger, Baggage |
| **SecurityCheckpoint** | 5 | 3 | MetalDetector, XRayScanner, SecurityOfficer, Passenger, Baggage |
| **PassportControl** | 2 | 1 | Passenger, Visa |
| **CustomsControl** | 2 | 1 | CustomsDeclaration |
| **WeatherReport** | 6 | 1 | — |
| **ServiceTask** | 4 | 6 | Aircraft, Employee |
| **MaintenanceInspection** | 4 | 6 | Aircraft |
| **RefuelingTask** | 6 | 6 | Aircraft, FuelTruck |
| **CleaningTask** | 5 | 6 | Aircraft |
| **CateringTask** | 6 | 6 | Aircraft |
| **AirportFacade** | 9 | 14 | Airport, Schedule, Passenger, Employee, Aircraft, FuelTruck, Ticket, SecurityCheckpoint, WeatherReport, DepartureFlight, BoardingPass, Runway |
| **DataSeeder** | 1 | 1 | AirportFacade, Runway, Terminal, Gate, PassengerAircraft, FuelTruck, Pilot, SecurityOfficer |
| **CLI** | 1 | 8 | AirportFacade, Passenger, CustomsControl, PassportControl |

---

## 2. Пользовательские исключения (14)

Архитектура содержит собственную иерархию исключений с базовым классом `AirportException`:

1. `AirportException` — базовое исключение доменной модели аэропорта.
2. `FlightDelayedException` — выбрасывается при попытке выполнить штатные операции с отложенным рейсом.
3. `BoardingClosedException` — выбрасывается при попытке посадки пассажира после закрытия гейта.
4. `InvalidTicketException` — выбрасывается при несовпадении данных билета и пассажира или отсутствии брони.
5. `BaggageOverweightException` — выбрасывается при превышении допустимого веса багажа.
6. `RunwayBusyException` — выбрасывается при попытке посадки или взлета на занятую взлетно-посадочную полосу.
7. `SecurityCheckFailedException` — выбрасывается, если пассажир или багаж не прошли досмотр службы безопасности.
8. `VisaExpiredException` — выбрасывается на пограничном контроле при отсутствии или просрочке визы.
9. `GateNotAssignedException` — выбрасывается при попытке начать посадку без привязки рейса к конкретному гейту.
10. `MaintenanceRequiredException` — выбрасывается при попытке отправить в рейс борт, не прошедший технический осмотр.
11. `NoAvailableCrewException` — выбрасывается при нехватке пилотов или бортпроводников для формирования экипажа.
12. `WeatherWarningException` — выбрасывается диспетчерской вышкой при запрете вылетов из-за плохих метеоусловий.
13. `CapacityExceededException` — выбрасывается при попытке продать билет на полностью заполненный рейс или переполнить зал ожидания.
14. `PassengerNotFoundException` — выбрасывается при поиске несуществующего пассажира в манифесте рейса.

---

## 3. Сводная статистика объектной модели

| Показатель | Требование задания | Фактическое значение |
|---|:---:|:---:|
| **Классы** | $\ge$ 50 | **70** |
| **Поля** | $\ge$ 150 | **327** |
| **Поведения (методы логики)** | $\ge$ 100 | **206** |
| **Ассоциации (связи между классами)** | $\ge$ 30 | **65** |
| **Собственные исключения** | $\ge$ 12 | **14** |

---

## 4. Документация

В проекте используется автоматическая генерация документации на основе встроенных docstrings с помощью утилиты **pdoc**. Папка `docs/` является артефактом сборки и не хранится в репозитории.

### Гайд по созданию документации:

1. Убедитесь, что у вас установлен Python-пакет `pdoc`. Если его нет, установите:
   ```bash
   pip install pdoc
   ```
2. Откройте терминал и перейдите в **корень всего репозитория** (`ppois_labs`):
   ```bash
   cd ~/CLionProjects/ppois_labs
   ```
3. Запустите генерацию, передав переменную окружения `PYTHONPATH=.`:
   ```bash
   PYTHONPATH=. pdoc lab3 -o lab3/docs
   ```
4. Утилита создаст папку `docs/`. Откройте главный файл в браузере:
   ```bash
   open lab3/docs/index.html
   ```

## 5. Сборка, тестирование и запуск

Выполняется из корня репозитория:
```bash
python -m pytest --cov=lab3/domain --cov-fail-under=90 lab3/tests/
```

### Статический анализ и проверка типов
```bash
ruff check lab3/
mypy lab3/ --explicitcd-package-bases --ignore-missing-imports
```

### Запуск консольного интерфейса (CLI)
```bash
python -m lab3.cli
```

### Сборка автономного исполняемого файла (.exe / binary)
Автоматическая сборка настроена через GitHub Actions. Для локальной сборки:
```bash
pyinstaller --onefile --name ppois_lab3 lab3/cli.py
```
Готовый исполняемый файл будет создан в каталоге `dist/`.
