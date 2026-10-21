# Laboratory Work No. 3. Object-Oriented Airport Architecture

Enterprise information management system for a major international airport. The system coordinates airport physical infrastructure (runways, passenger terminals, boarding gates), the aviation and ground vehicle fleet (passenger airliners, cargo aircraft, private jets, fuel trucks, baggage tractors, apron buses), personnel and passenger rosters, operational workflows (flight schedules, e-ticketing, baggage handling, boarding passes), aviation security (metal detectors, X-ray scanners, customs and passport border control), and comprehensive ground maintenance (line inspections, refueling, interior cleaning, catering, weather dispatching).

---

## 1. Object Model & Class Specification

*Note: The "Fields" and "Methods" columns reflect instance attributes initialized in __init__ and public domain behaviors (excluding getters/setters and dunder methods) defined in each class.*

### 1.1 Transport Fleet (`lab3/domain/fleet/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **fleet/vehicle.py** | `Vehicle` | 4 | 3 | — |
| **fleet/aircraft.py** | `Aircraft` | 5 | 4 | `Vehicle` |
| **fleet/passenger_aircraft.py** | `PassengerAircraft` | 4 | 3 | `Aircraft` |
| **fleet/cargo_aircraft.py** | `CargoAircraft` | 4 | 3 | `Aircraft` |
| **fleet/private_jet.py** | `PrivateJet` | 3 | 3 | `Aircraft` |
| **fleet/ground_vehicle.py** | `GroundVehicle` | 2 | 3 | `Vehicle` |
| **fleet/baggage_tractor.py** | `BaggageTractor` | 3 | 4 | `Baggage`, `GroundVehicle` |
| **fleet/fuel_truck.py** | `FuelTruck` | 4 | 3 | `Aircraft`, `GroundVehicle` |
| **fleet/follow_me_car.py** | `FollowMeCar` | 2 | 3 | `Aircraft`, `GroundVehicle` |
| **fleet/passenger_bus.py** | `PassengerBus` | 3 | 4 | `GroundVehicle`, `Passenger` |

### 1.2 Airport Infrastructure (`lab3/domain/infrastructure/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **infrastructure/runway.py** | `Runway` | 4 | 2 | `Aircraft` |
| **infrastructure/gate.py** | `Gate` | 3 | 4 | `Flight` |
| **infrastructure/check_in_counter.py** | `CheckInCounter` | 5 | 3 | `Baggage`, `CheckInAgent`, `Flight` |
| **infrastructure/baggage_carousel.py** | `BaggageCarousel` | 3 | 2 | `Flight` |
| **infrastructure/lounge.py** | `Lounge` | 4 | 2 | `Passenger` |
| **infrastructure/terminal.py** | `Terminal` | 5 | 5 | `BaggageCarousel`, `CheckInCounter`, `Gate`, `Lounge` |
| **infrastructure/control_tower.py** | `ControlTower` | 3 | 4 | `Aircraft`, `Runway` |
| **infrastructure/hangar.py** | `Hangar` | 3 | 2 | `Aircraft` |
| **infrastructure/parking_lot.py** | `ParkingLot` | 3 | 2 | `GroundVehicle` |
| **infrastructure/airport.py** | `Airport` | 6 | 2 | `ControlTower`, `Hangar`, `ParkingLot`, `Terminal` |

### 1.3 Ground Maintenance (`lab3/domain/maintenance/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **maintenance/weather_report.py** | `WeatherReport` | 6 | 3 | — |
| **maintenance/service_task.py** | `ServiceTask` | 4 | 6 | `Aircraft`, `Employee` |
| **maintenance/maintenance_inspection.py** | `MaintenanceInspection` | 3 | 3 | `Aircraft`, `ServiceTask` |
| **maintenance/refueling_task.py** | `RefuelingTask` | 2 | 3 | `Aircraft`, `FuelTruck`, `ServiceTask` |
| **maintenance/cleaning_task.py** | `CleaningTask` | 3 | 2 | `Aircraft`, `ServiceTask` |
| **maintenance/catering_task.py** | `CateringTask` | 2 | 2 | `Aircraft`, `ServiceTask` |

### 1.4 Flight Operations (`lab3/domain/operations/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **operations/baggage.py** | `Baggage` | 4 | 3 | `Passenger` |
| **operations/ticket.py** | `Ticket` | 6 | 3 | `Flight`, `Passenger` |
| **operations/boarding_pass.py** | `BoardingPass` | 5 | 5 | `Gate`, `Ticket` |
| **operations/airline.py** | `Airline` | 3 | 3 | `Aircraft` |
| **operations/flight_plan.py** | `FlightPlan` | 5 | 3 | — |
| **operations/flight.py** | `Flight` | 10 | 5 | `Aircraft`, `Airline`, `CrewMember`, `FlightPlan`, `Gate`, `Passenger`, `Runway` |
| **operations/departure_flight.py** | `DepartureFlight` | 4 | 7 | `Aircraft`, `Airline`, `Baggage`, `BoardingPass`, `Flight`, `FlightPlan`, `Gate`, `Passenger`, `Pilot`, `Ticket` |
| **operations/arrival_flight.py** | `ArrivalFlight` | 3 | 3 | `Aircraft`, `Airline`, `BaggageCarousel`, `Flight`, `FlightPlan` |
| **operations/schedule.py** | `Schedule` | 3 | 4 | `ArrivalFlight`, `DepartureFlight`, `Flight` |

### 1.5 Personnel and Passengers (`lab3/domain/people/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **people/person.py** | `Person` | 4 | 3 | — |
| **people/passenger.py** | `Passenger` | 3 | 5 | `Baggage`, `Person`, `Ticket` |
| **people/employee.py** | `Employee` | 3 | 4 | `Person` |
| **people/crew_member.py** | `CrewMember` | 2 | 3 | `Employee` |
| **people/pilot.py** | `Pilot` | 3 | 3 | `CrewMember`, `FlightPlan` |
| **people/flight_attendant.py** | `FlightAttendant` | 2 | 4 | `CrewMember`, `Passenger` |
| **people/dispatcher.py** | `Dispatcher` | 3 | 3 | `Employee`, `Flight` |
| **people/security_officer.py** | `SecurityOfficer` | 2 | 3 | `Employee`, `Passenger` |
| **people/check_in_agent.py** | `CheckInAgent` | 3 | 3 | `Baggage`, `Employee`, `Flight`, `Passenger` |
| **people/baggage_handler.py** | `BaggageHandler` | 2 | 3 | `Baggage`, `Employee`, `Flight` |

### 1.6 Border & Aviation Security (`lab3/domain/security/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **security/visa.py** | `Visa` | 4 | 3 | — |
| **security/customs_declaration.py** | `CustomsDeclaration` | 5 | 4 | `Passenger` |
| **security/scanner.py** | `Scanner` | 4 | 3 | `Baggage`, `Passenger` |
| **security/metal_detector.py** | `MetalDetector` | 2 | 3 | `Baggage`, `Passenger`, `Scanner` |
| **security/xray_scanner.py** | `XRayScanner` | 3 | 3 | `Baggage`, `Passenger`, `Scanner` |
| **security/security_checkpoint.py** | `SecurityCheckpoint` | 6 | 7 | `Baggage`, `MetalDetector`, `Passenger`, `SecurityOfficer`, `XRayScanner` |
| **security/passport_control.py** | `PassportControl` | 2 | 3 | `Passenger`, `Visa` |
| **security/customs_control.py** | `CustomsControl` | 2 | 3 | `CustomsDeclaration`, `Passenger` |

### 1.7 Main Facade Controller (`lab3/domain/facade/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **facade/airport_facade.py** | `AirportFacade` | 7 | 16 | `Aircraft`, `Airline`, `Airport`, `Baggage`, `BoardingPass`, `DepartureFlight`, `Employee`, `FlightPlan`, `FuelTruck`, `MaintenanceInspection`, `MetalDetector`, `Passenger`, `RefuelingTask`, `Runway`, `Schedule`, `SecurityCheckpoint`, `Ticket`, `WeatherReport`, `XRayScanner` |

---

## 2. Custom Domain Exceptions (14)

The architecture contains an isolated domain exception hierarchy rooted in `AirportException`:

1. `AirportException` — Base exception class for the airport domain model.
2. `FlightDelayedException` — Raised when attempting standard operational procedures on a delayed flight.
3. `BoardingClosedException` — Raised when a passenger attempts to board after gate closure.
4. `InvalidTicketException` — Raised when ticket verification fails or a duplicate check-in occurs.
5. `BaggageOverweightException` — Raised when checked luggage exceeds maximum baggage allowance.
6. `RunwayBusyException` — Raised when an aircraft requests takeoff or landing on an occupied runway.
7. `SecurityCheckFailedException` — Raised when a passenger or baggage item fails screening.
8. `VisaExpiredException` — Raised at border control when an entry visa is expired or absent.
9. `GateNotAssignedException` — Raised when attempting to board without an allocated departure gate.
10. `MaintenanceRequiredException` — Raised when an aircraft attempts flight without line maintenance clearance.
11. `NoAvailableCrewException` — Raised when minimum flight crew requirements are not satisfied.
12. `WeatherWarningException` — Raised by air traffic control when severe weather conditions prohibit operations.
13. `CapacityExceededException` — Raised when flight booking limits, lounge capacity, or vehicle thresholds are breached.
14. `PassengerNotFoundException` — Raised when querying a passenger absent from manifests or registries.

---

## 3. Summary Object Model Statistics

*Note: The "Fields" and "Methods" columns reflect instance attributes initialized in __init__ and public domain behaviors (excluding getters/setters and dunder methods) defined in each class.*

| Metric | Assignment Requirement | Actual Value |
|---|:---:|:---:|
| **Classes** | $\ge$ 50 | **68** |
| **Attributes / Fields** | $\ge$ 150 | **198** |
| **Behaviors / Methods** | $\ge$ 100 | **195** |
| **Class Associations** | $\ge$ 30 | **131** |
| **Custom Domain Exceptions** | $\ge$ 12 | **14** |

---

## 4. Documentation Generation

The project utilizes automated API documentation generation via **pdoc**, parsing standard docstrings across all modules. The `docs/` directory is treated as a build artifact and excluded from version control.

### Guide to Generating Documentation:

1. Ensure the `pdoc` package is installed in your virtual environment:
   ```bash
   pip install pdoc
   ```
2. Open a terminal and navigate to the **repository root**:
   ```bash
   cd ~/CLionProjects/ppois_labs
   ```
3. Execute HTML documentation generation:
   ```bash
   PYTHONPATH=. pdoc lab3 -o lab3/docs
   ```
4. Open the generated entrypoint in your browser:
   ```bash
   open lab3/docs/index.html
   ```

---

## 5. Testing, Linting & Build Procedures

All commands must be executed from the repository root:

### Run Unit Tests & Verify Code Coverage (90%+ Required)
```bash
python -m pytest --cov=lab3/domain --cov-fail-under=90 lab3/tests/ -v
```

### Static Analysis & Strict Type Checking
```bash
ruff check lab3/
mypy lab3/ --explicit-package-bases --ignore-missing-imports
```
