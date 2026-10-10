# Laboratory Work No. 3. Object-Oriented Airport Architecture

Enterprise information management system for a major international airport. The system coordinates airport physical infrastructure (runways, passenger terminals, boarding gates), the aviation and ground vehicle fleet (passenger airliners, cargo aircraft, private jets, fuel trucks, baggage tractors, apron buses), personnel and passenger rosters, operational workflows (flight schedules, e-ticketing, baggage handling, boarding passes), aviation security (metal detectors, X-ray scanners, customs and passport border control), and comprehensive ground maintenance (line inspections, refueling, interior cleaning, catering, weather dispatching).

---

## 1. Object Model & Class Specification

*Note: The "Fields" and "Methods" columns include all class variables, properties, initialized instance variables, and inherited attributes/methods from parent classes to reflect the exact memory and behavior footprint of each instantiated object.*

### 1.1 Transport Fleet (`lab3/domain/fleet/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **fleet/vehicle.py** | `Vehicle` | 5 | 1 | — |
| **fleet/aircraft.py** | `Aircraft` | 9 | 5 | — |
| **fleet/passenger_aircraft.py** | `PassengerAircraft` | 13 | 8 | — |
| **fleet/cargo_aircraft.py** | `CargoAircraft` | 13 | 8 | — |
| **fleet/private_jet.py** | `PrivateJet` | 12 | 6 | — |
| **fleet/ground_vehicle.py** | `GroundVehicle` | 7 | 3 | — |
| **fleet/baggage_tractor.py** | `BaggageTractor` | 10 | 6 | — |
| **fleet/fuel_truck.py** | `FuelTruck` | 11 | 5 | `Aircraft` |
| **fleet/follow_me_car.py** | `FollowMeCar` | 8 | 4 | `Aircraft` |
| **fleet/passenger_bus.py** | `PassengerBus` | 10 | 6 | — |

### 1.2 Airport Infrastructure (`lab3/domain/infrastructure/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **infrastructure/runway.py** | `Runway` | 5 | 2 | `Aircraft` |
| **infrastructure/gate.py** | `Gate` | 4 | 4 | `Flight` |
| **infrastructure/check_in_counter.py** | `CheckInCounter` | 6 | 3 | `CheckInAgent`, `Flight`, `Baggage` |
| **infrastructure/baggage_carousel.py** | `BaggageCarousel` | 4 | 2 | `Flight` |
| **infrastructure/lounge.py** | `Lounge` | 5 | 3 | `Passenger` |
| **infrastructure/terminal.py** | `Terminal` | 6 | 5 | `Gate`, `CheckInCounter`, `BaggageCarousel`, `Lounge` |
| **infrastructure/control_tower.py** | `ControlTower` | 3 | 4 | `Runway`, `Aircraft` |
| **infrastructure/hangar.py** | `Hangar` | 4 | 2 | `Aircraft` |
| **infrastructure/parking_lot.py** | `ParkingLot` | 4 | 2 | — |
| **infrastructure/airport.py** | `Airport` | 6 | 2 | `ControlTower`, `Terminal`, `Hangar`, `ParkingLot` |

### 1.3 Ground Maintenance (`lab3/domain/maintenance/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **maintenance/weather_report.py** | `WeatherReport` | 6 | 1 | — |
| **maintenance/service_task.py** | `ServiceTask` | 4 | 6 | `Aircraft`, `Employee` |
| **maintenance/maintenance_inspection.py** | `MaintenanceInspection` | 4 | 6 | `Aircraft`, `Employee` |
| **maintenance/refueling_task.py** | `RefuelingTask` | 6 | 6 | `Aircraft`, `FuelTruck`, `Employee` |
| **maintenance/cleaning_task.py** | `CleaningTask` | 5 | 6 | `Aircraft`, `Employee` |
| **maintenance/catering_task.py** | `CateringTask` | 6 | 6 | `Aircraft`, `Employee` |

### 1.4 Flight Operations (`lab3/domain/operations/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **operations/baggage.py** | `Baggage` | 4 | 1 | `Passenger` |
| **operations/ticket.py** | `Ticket` | 8 | 1 | `Passenger`, `Flight` |
| **operations/boarding_pass.py** | `BoardingPass` | 5 | 0 | `Ticket`, `Gate` |
| **operations/airline.py** | `Airline` | 4 | 3 | `Aircraft` |
| **operations/flight_plan.py** | `FlightPlan` | 5 | 0 | — |
| **operations/flight.py** | `Flight` | 7 | 2 | `Airline`, `Aircraft`, `FlightPlan` |
| **operations/departure_flight.py** | `DepartureFlight` | 11 | 8 | `Gate`, `Passenger`, `Baggage`, `Ticket`, `BoardingPass`, `Airline`, `Aircraft`, `FlightPlan` |
| **operations/arrival_flight.py** | `ArrivalFlight` | 8 | 4 | `BaggageCarousel`, `Airline`, `Aircraft`, `FlightPlan` |
| **operations/schedule.py** | `Schedule` | 1 | 3 | `Flight`, `DepartureFlight`, `ArrivalFlight` |

### 1.5 Personnel and Passengers (`lab3/domain/people/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **people/person.py** | `Person` | 4 | 1 | — |
| **people/passenger.py** | `Passenger` | 7 | 6 | `Ticket`, `Baggage` |
| **people/employee.py** | `Employee` | 7 | 4 | — |
| **people/crew_member.py** | `CrewMember` | 9 | 6 | — |
| **people/pilot.py** | `Pilot` | 12 | 6 | — |
| **people/flight_attendant.py** | `FlightAttendant` | 11 | 6 | — |
| **people/dispatcher.py** | `Dispatcher` | 9 | 4 | — |
| **people/security_officer.py** | `SecurityOfficer` | 7 | 4 | — |
| **people/check_in_agent.py** | `CheckInAgent` | 9 | 5 | — |
| **people/baggage_handler.py** | `BaggageHandler` | 9 | 5 | — |

### 1.6 Border & Aviation Security (`lab3/domain/security/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **security/visa.py** | `Visa` | 3 | 1 | — |
| **security/customs_declaration.py** | `CustomsDeclaration` | 6 | 2 | `Passenger` |
| **security/scanner.py** | `Scanner` | 3 | 1 | `Passenger`, `Baggage` |
| **security/metal_detector.py** | `MetalDetector` | 3 | 1 | `Passenger`, `Baggage` |
| **security/xray_scanner.py** | `XRayScanner` | 3 | 1 | `Passenger`, `Baggage` |
| **security/security_checkpoint.py** | `SecurityCheckpoint` | 5 | 3 | `MetalDetector`, `XRayScanner`, `SecurityOfficer`, `Passenger`, `Baggage` |
| **security/passport_control.py** | `PassportControl` | 2 | 1 | `Passenger`, `Visa` |
| **security/customs_control.py** | `CustomsControl` | 2 | 1 | `CustomsDeclaration` |

### 1.7 Main Facade Controller (`lab3/domain/facade/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **facade/airport_facade.py** | `AirportFacade` | 9 | 14 | `Airport`, `Schedule`, `Passenger`, `Employee`, `Aircraft`, `FuelTruck`, `Ticket`, `SecurityCheckpoint`, `WeatherReport`, `DepartureFlight`, `BoardingPass`, `Runway`, `Airline`, `FlightPlan`, `Baggage` |

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

*Note: The statistics below represent the exact sums computed directly from the 54 domain classes in the sub-tables above combined with the 14 custom exception classes.*

| Metric | Assignment Requirement | Actual Value |
|---|:---:|:---:|
| **Classes** | $\ge$ 50 | **68** |
| **Attributes / Fields** | $\ge$ 150 | **349** |
| **Behaviors / Methods** | $\ge$ 100 | **206** |
| **Class Associations** | $\ge$ 30 | **87** |
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
