# Laboratory Work No. 2. Object-Oriented Dean's Office Architecture

University dean's office information management system. The system models the administrative workflows of a higher education faculty: student registration, teaching personnel, academic disciplines, course schedules, examination grading and credit books, official dean's orders, campus facilities (dormitories, library catalog), and student financial accounts.

---

## 1. Object Model & Class Specification

*Note: The "Fields" and "Methods" columns include all class variables, properties, initialized instance variables, and inherited attributes/methods from parent classes to reflect the exact memory and behavior footprint of each instantiated object.*

### 1.1 Academic Process (`lab2/domain/academics/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **academics/labwork.py** | `LabWork` | 6 | 4 | `Subject` |
| **academics/subject.py** | `Subject` | 5 | 6 | `LabWork` |

### 1.2 Personnel and Students (`lab2/domain/people/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **people/person.py** | `Person` | 5 | 4 | `BankAccount` |
| **people/student.py** | `Student` | 13 | 8 | `RecordBook`, `AcademicGroup`, `Room`, `LibraryCard`, `BankAccount` |
| **people/employee.py** | `Employee` | 7 | 6 | `BankAccount` |
| **people/lecturer.py** | `Lecturer` | 12 | 10 | `Department`, `Subject`, `BankAccount` |
| **people/dean.py** | `Dean` | 10 | 7 | `BankAccount` |
| **people/assistant.py** | `Assistant` | 12 | 10 | `Department`, `Subject`, `BankAccount` |
| **people/associate_professor.py** | `AssociateProfessor` | 12 | 10 | `Department`, `Subject`, `BankAccount` |
| **people/professor.py** | `Professor` | 12 | 10 | `Department`, `Subject`, `BankAccount` |

### 1.3 Financial Operations (`lab2/domain/finance/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **finance/bank_account.py** | `BankAccount` | 6 | 5 | `Person` |
| **finance/tuition_contract.py** | `TuitionContract` | 10 | 8 | `Student`, `BankAccount` |
| **finance/payroll.py** | `Payroll` | 5 | 5 | `Employee`, `Student`, `BankAccount` |

### 1.4 Examination & Grading (`lab2/domain/grading/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **grading/grade.py** | `Grade` | 8 | 3 | `Subject` |
| **grading/record_book.py** | `RecordBook` | 4 | 8 | `Student`, `Grade`, `Subject` |
| **grading/academic_statement.py** | `AcademicStatement` | 6 | 4 | `Subject`, `AcademicGroup`, `Lecturer`, `Student`, `Grade` |
| **grading/retake_sheet.py** | `RetakeSheet` | 7 | 2 | `Student`, `Subject`, `Grade` |

### 1.5 Academic Structure (`lab2/domain/structure/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **structure/speciality.py** | `Speciality` | 6 | 3 | — |
| **structure/academic_group.py** | `AcademicGroup` | 5 | 10 | `Speciality`, `Student` |
| **structure/department.py** | `Department` | 4 | 5 | `Lecturer` |
| **structure/faculty.py** | `Faculty` | 4 | 8 | `Department`, `AcademicGroup`, `Student` |
| **structure/university.py** | `University` | 3 | 3 | `Faculty` |

### 1.6 Campus Infrastructure (`lab2/domain/infrastructure/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **infrastructure/room.py** | `Room` | 4 | 7 | `Student` |
| **infrastructure/dormitory.py** | `Dormitory` | 3 | 5 | `Room`, `Student` |

### 1.7 Library Services (`lab2/domain/library/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **library/book.py** | `Book` | 6 | 5 | — |
| **library/library_card.py** | `LibraryCard` | 4 | 5 | `Student`, `Book` |

### 1.8 Course Scheduling (`lab2/domain/schedule/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **schedule/classroom.py** | `Classroom` | 6 | 5 | — |
| **schedule/timeslot.py** | `Timeslot` | 3 | 2 | — |
| **schedule/lesson.py** | `Lesson` | 7 | 3 | `Subject`, `Lecturer`, `AcademicGroup`, `Classroom`, `Timeslot` |
| **schedule/timetable.py** | `Timetable` | 2 | 5 | `Lesson`, `AcademicGroup`, `Lecturer` |

### 1.9 Administrative Orders & Documents (`lab2/domain/documents/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **documents/document.py** | `Document` | 5 | 5 | `Dean` |
| **documents/expulsion_order.py** | `ExpulsionOrder` | 7 | 6 | `Student`, `Dean` |
| **documents/academic_certificate.py** | `AcademicCertificate` | 7 | 5 | `Student`, `Dean` |
| **documents/transfer_order.py** | `TransferOrder` | 8 | 6 | `Student`, `AcademicGroup`, `Dean` |
| **documents/scholarship_order.py** | `ScholarshipOrder` | 6 | 6 | `Student`, `Dean` |
| **documents/academic_leave_order.py** | `AcademicLeaveOrder` | 8 | 6 | `Student`, `Dean` |
| **documents/reprimand_order.py** | `ReprimandOrder` | 8 | 6 | `Student`, `Dean` |

### 1.10 Main Faculty Controller (`lab2/domain/dean_office/`)

| Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **dean_office/dean_office.py** | `DeanOffice` | 6 | 10 | `Faculty`, `Dean`, `RecordBook`, `Student`, `AcademicGroup`, `Document`, `ExpulsionOrder`, `ReprimandOrder`, `ScholarshipOrder`, `TransferOrder` |

---

## 2. Custom Domain Exceptions (14)

The architecture contains an isolated domain exception hierarchy rooted in `DeanOfficeException`:

1. `DeanOfficeException` — Base exception class for the dean's office domain model.
2. `StudentNotFoundException` — Raised when a student or record book cannot be found in the registry.
3. `GroupNotFoundException` — Raised when an academic group is absent from the faculty roster.
4. `DuplicateEnrollmentException` — Raised when attempting to enroll a student already present in the target group.
5. `ExpulsionDeniedException` — Raised when attempting to execute an expulsion order lacking valid academic or legal grounds.
6. `InsufficientFundsException` — Raised when a bank account balance is insufficient for withdrawal or transfer.
7. `AccountBlockedException` — Raised when an operation is attempted on a blocked bank account.
8. `InvalidScoreException` — Raised when an academic grade falls outside the allowed 0–10 scale.
9. `RoomCapacityExceededException` — Raised when attempting to check a student into a fully occupied dormitory room.
10. `ResidentNotFoundException` — Raised when attempting to evict a student who is not registered in the specified room.
11. `BookNotAvailableException` — Raised when no available copies of a book remain in the library inventory.
12. `LibraryLimitExceededException` — Raised when a student exceeds the maximum limit for simultaneously borrowed books.
13. `ScheduleCollisionException` — Raised when an overlap occurs regarding an auditorium, lecturer, or group in the schedule.
14. `DocumentNotSignedException` — Raised when attempting to execute an order without the dean's signature.

---

## 3. Summary Object Model Statistics

*Note: The statistics below represent the exact sums computed directly from the 38 domain classes in the sub-tables above combined with the 14 custom exception classes.*

| Metric | Assignment Requirement | Actual Value |
|---|:---:|:---:|
| **Classes** | $\ge$ 50 | **52** |
| **Attributes / Fields** | $\ge$ 150 | **252** |
| **Behaviors / Methods** | $\ge$ 100 | **226** |
| **Class Associations** | $\ge$ 30 | **84** |
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
   PYTHONPATH=. pdoc lab2 -o lab2/docs
   ```
4. Open the generated entrypoint in your browser:
   ```bash
   open lab2/docs/index.html
   ```

---

## 5. Testing, Linting & Build Procedures

All commands must be executed from the repository root:

### Run Unit Tests & Verify Code Coverage (90%+ Required)
```bash
python -m pytest --cov=lab2/domain --cov-fail-under=90 lab2/tests/ -v
```

### Static Analysis & Strict Type Checking
```bash
ruff check lab2/
mypy lab2/ --explicit-package-bases --ignore-missing-imports
```
