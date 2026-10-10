# Laboratory Work No. 2. Object-Oriented Dean's Office Architecture

University dean's office information management system. The system models the administrative workflows of a higher education faculty: student registration, teaching personnel, academic disciplines, course schedules, examination grading and credit books, official dean's orders, campus facilities (dormitories, library catalog), and student financial accounts.

---

## 1. Object Model & Class Specification

*Note: In the "Fields" column, subclass counts include all attributes inherited from their respective parent classes.*

| Subpackage & Module Path | Class | Fields | Methods | Associations (Connected Classes) |
|---|---|:---:|:---:|---|
| **academics/labwork.py** | `LabWork` | 6 | 3 | `Subject` |
| **academics/subject.py** | `Subject` | 5 | 5 | `LabWork` |
| **people/person.py** | `Person` | 5 | 3 | `BankAccount` |
| **people/student.py** | `Student` | 13 | 4 | `RecordBook`, `AcademicGroup`, `Room`, `LibraryCard`, `BankAccount` |
| **people/employee.py** | `Employee` | 7 | 3 | `BankAccount` |
| **people/lecturer.py** | `Lecturer` | 12 | 5 | `Department`, `Subject`, `BankAccount` |
| **people/dean.py** | `Dean` | 10 | 2 | `BankAccount` |
| **people/assistant.py** | `Assistant` | 12 | 1 | `Department`, `Subject`, `BankAccount` |
| **people/associate_professor.py** | `AssociateProfessor` | 12 | 1 | `Department`, `Subject`, `BankAccount` |
| **people/professor.py** | `Professor` | 12 | 1 | `Department`, `Subject`, `BankAccount` |
| **finance/bank_account.py** | `BankAccount` | 6 | 5 | `Person` |
| **finance/tuition_contract.py** | `TuitionContract` | 10 | 7 | `Student`, `BankAccount` |
| **finance/payroll.py** | `Payroll` | 5 | 4 | `Employee`, `Student`, `BankAccount` |
| **grading/grade.py** | `Grade` | 8 | 3 | `Subject` |
| **grading/record_book.py** | `RecordBook` | 4 | 7 | `Student`, `Grade`, `Subject` |
| **grading/academic_statement.py** | `AcademicStatement` | 6 | 4 | `Subject`, `AcademicGroup`, `Lecturer`, `Student`, `Grade` |
| **grading/retake_sheet.py** | `RetakeSheet` | 7 | 2 | `Student`, `Subject`, `Grade` |
| **structure/speciality.py** | `Speciality` | 6 | 3 | — |
| **structure/academic_group.py** | `AcademicGroup` | 5 | 9 | `Speciality`, `Student` |
| **structure/department.py** | `Department` | 4 | 5 | `Lecturer` |
| **structure/faculty.py** | `Faculty` | 4 | 8 | `Department`, `AcademicGroup`, `Student` |
| **structure/university.py** | `University` | 3 | 3 | `Faculty` |
| **infrastructure/room.py** | `Room` | 4 | 6 | `Student` |
| **infrastructure/dormitory.py** | `Dormitory` | 3 | 5 | `Room`, `Student` |
| **library/book.py** | `Book` | 6 | 5 | — |
| **library/library_card.py** | `LibraryCard` | 4 | 5 | `Student`, `Book` |
| **schedule/classroom.py** | `Classroom` | 6 | 5 | — |
| **schedule/timeslot.py** | `Timeslot` | 3 | 2 | — |
| **schedule/lesson.py** | `Lesson` | 7 | 3 | `Subject`, `Lecturer`, `AcademicGroup`, `Classroom`, `Timeslot` |
| **schedule/timetable.py** | `Timetable` | 2 | 5 | `Lesson`, `AcademicGroup`, `Lecturer` |
| **documents/document.py** | `Document` | 5 | 5 | `Dean` |
| **documents/expulsion_order.py** | `ExpulsionOrder` | 7 | 2 | `Student`, `Dean` |
| **documents/academic_certificate.py** | `AcademicCertificate` | 7 | 1 | `Student`, `Dean` |
| **documents/transfer_order.py** | `TransferOrder` | 8 | 2 | `Student`, `AcademicGroup`, `Dean` |
| **documents/scholarship_order.py** | `ScholarshipOrder` | 6 | 2 | `Student`, `Dean` |
| **documents/academic_leave_order.py** | `AcademicLeaveOrder` | 8 | 2 | `Student`, `Dean` |
| **documents/reprimand_order.py** | `ReprimandOrder` | 8 | 2 | `Student`, `Dean` |
| **dean_office/dean_office.py** | `DeanOffice` | 6 | 10 | `Faculty`, `Dean`, `RecordBook`, `Student`, `AcademicGroup`, `Document`, `ExpulsionOrder`, `ReprimandOrder`, `ScholarshipOrder`, `TransferOrder` |
| **cli.py** | `DataSeeder` | 1 | 1 | `DeanOffice`, `Faculty`, `Dormitory`, `TuitionContract`, `Book` |
| **cli.py** | `CLI` | 2 | 8 | `DeanOffice`, `Student`, `Subject`, `Grade`, `RetakeSheet`, `Payroll` |

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

| Metric | Assignment Requirement | Actual Value |
|---|:---:|:---:|
| **Classes** | $\ge$ 50 | **54** |
| **Attributes / Fields** | $\ge$ 150 | **268** |
| **Behaviors / Methods** | $\ge$ 100 | **162** |
| **Class Associations** | $\ge$ 30 | **61** |
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

### Run Interactive Console Application (CLI)
```bash
python -m lab2.cli
```

### Build Standalone Executable Binary
Automated builds are handled via GitHub Actions upon pushing to the repository. For local compilation using PyInstaller:
```bash
pyinstaller --onefile --paths . --collect-all lab2 --name ppois_lab2 lab2/cli.py
```
The output binary will be located inside the `dist/` directory.
