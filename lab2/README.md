# Лабораторная работа №2. Объектно-ориентированная архитектура деканата

Информационная система деканата университета. Система управляет структурой факультета, контингентом студентов, профессорско-преподавательским составом, учебным процессом, расписанием, сессионными ведомостями, приказами, инфраструктурой (общежитие, библиотека) и финансовыми взаиморасчетами.

---

## 1. Спецификация классов объектной модели

*Примечание: в столбце «Поля» для дочерних классов учитываются атрибуты, унаследованные от базовых.*

| Класс | Поля | Методы | Ассоциации (связанные классы) |
|---|:---:|:---:|---|
| **Person** | 4 | 3 | — |
| **Student** | 8 | 4 | — |
| **Employee** | 6 | 2 | — |
| **Lecturer** | 8 | 4 | — |
| **Dean** | 7 | 1 | — |
| **Assistant** | 8 | 0 | — |
| **AssociateProfessor** | 8 | 0 | — |
| **Professor** | 8 | 0 | — |
| **Speciality** | 3 | 2 | — |
| **AcademicGroup** | 4 | 9 | Speciality, Student |
| **Department** | 3 | 4 | Lecturer |
| **Faculty** | 4 | 7 | Department, AcademicGroup, Student |
| **University** | 3 | 2 | Faculty |
| **LabWork** | 4 | 3 | — |
| **Subject** | 5 | 5 | LabWork |
| **Grade** | 4 | 2 | — |
| **RecordBook** | 3 | 6 | Grade |
| **AcademicStatement** | 6 | 3 | Subject, AcademicGroup, Lecturer, Student, Grade |
| **RetakeSheet** | 6 | 1 | Student, Subject, Grade |
| **Document** | 5 | 4 | Dean |
| **ExpulsionOrder** | 7 | 1 | Document, Student |
| **TransferOrder** | 8 | 1 | Document, Student, AcademicGroup |
| **ScholarshipOrder** | 6 | 1 | Document, Student |
| **AcademicLeaveOrder** | 8 | 1 | Document, Student |
| **ReprimandOrder** | 8 | 1 | Document, Student |
| **AcademicCertificate** | 7 | 0 | Document, Student |
| **Room** | 3 | 6 | Student |
| **Dormitory** | 3 | 4 | Room, Student |
| **BankAccount** | 5 | 4 | BankAccount |
| **TuitionContract** | 7 | 7 | Student, BankAccount |
| **Payroll** | 4 | 4 | Employee, Student, BankAccount |
| **Classroom** | 6 | 4 | — |
| **Timeslot** | 3 | 1 | — |
| **Lesson** | 7 | 2 | Subject, Lecturer, AcademicGroup, Classroom, Timeslot |
| **Timetable** | 2 | 4 | Lesson, AcademicGroup, Lecturer |
| **Book** | 6 | 4 | — |
| **LibraryCard** | 3 | 4 | Student, Book |
| **DeanOffice** | 4 | 9 | Faculty, Dean, RecordBook, Student, AcademicGroup, Document |
| **DataSeeder** | 1 | 1 | DeanOffice, Faculty, Dormitory, TuitionContract, Book |
| **CLI** | 2 | 8 | DeanOffice, Student, Subject, Grade, RetakeSheet, Payroll |

---

## 2. Пользовательские исключения (14)

Архитектура содержит собственную иерархию исключений с базовым классом `DeanOfficeException`:

1. `DeanOfficeException` — базовое доменное исключение подсистемы деканата.
2. `StudentNotFoundException` — студент или зачетная книжка не найдены в реестре.
3. `GroupNotFoundException` — учебная группа с заданным номером отсутствует на факультете.
4. `DuplicateEnrollmentException` — попытка повторного зачисления студента в группу.
5. `ExpulsionDeniedException` — отказ в отчислении при отсутствии законных оснований.
6. `InsufficientFundsException` — недостаточно средств на счете для проведения транзакции.
7. `AccountBlockedException` — попытка проведения операции по заблокированному счету.
8. `InvalidScoreException` — выход выставляемой оценки за допустимый диапазон.
9. `RoomCapacityExceededException` — превышение лимита мест в комнате общежития.
10. `ResidentNotFoundException` — студент не числится проживающим в данном блоке.
11. `BookNotAvailableException` — отсутствие доступных экземпляров книги в фонде библиотеки.
12. `LibraryLimitExceededException` — превышение лимита одновременно взятых книг.
13. `ScheduleCollisionException` — накладка по аудитории, преподавателю или группе в расписании.
14. `DocumentNotSignedException` — попытка исполнения неподписанного приказа.

---

## 3. Сводная статистика объектной модели

| Показатель | Требование задания | Фактическое значение |
|---|:---:|:---:|
| **Классы** | $\ge$ 50 | **54** |
| **Поля** | $\ge$ 150 | **208** |
| **Поведения (методы логики)** | $\ge$ 100 | **129** |
| **Ассоциации (связи между классами)** | $\ge$ 30 | **42** |
| **Собственные исключения** | $\ge$ 12 | **14** |

---

## 4. Инструкция по сборке, тестированию и запуску

### Запуск unit-тестов с проверкой покрытия (>90%)
```bash
python -m pytest --cov=lab2/domain --cov-fail-under=90 lab2/tests/
```

### Статический анализ и проверка типов
```bash
ruff check lab2/
mypy lab2/ --explicit-package-bases --ignore-missing-imports
```

### Запуск консольного интерфейса (CLI)
```bash
python -m lab2.cli
```

### Сборка автономного исполняемого файла (.exe / binary)
Автоматическая сборка настроена через GitHub Actions при пуше в репозиторий (доступно в разделе Releases). Для локальной сборки:
```bash
pyinstaller --onefile --name ppois_lab2 lab2/cli.py
```
Готовый исполняемый файл создается в каталоге `dist/`.
