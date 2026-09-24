#       python -m pytest lab2/tests/test_domain.py --cov=lab2/domain --cov-report=term-missing


import pytest
from datetime import datetime

# Импорты всех моделей
from lab2.domain.academics import LabWork, Subject
from lab2.domain.people import Person, Student, Employee, Lecturer, Dean, Assistant, Professor
from lab2.domain.structure import Speciality, AcademicGroup, Department, Faculty, University
from lab2.domain.grading import Grade, RecordBook, AcademicStatement, RetakeSheet
from lab2.domain.documents import Document, ExpulsionOrder, TransferOrder, ScholarshipOrder, ReprimandOrder, \
    AcademicLeaveOrder
from lab2.domain.finance import BankAccount, TuitionContract, Payroll
from lab2.domain.infrastructure import Room, Dormitory
from lab2.domain.library import Book, LibraryCard
from lab2.domain.schedule import Classroom, Timeslot, Lesson, Timetable
from lab2.domain.dean_office import DeanOffice

# Импорты кастомных исключений
from lab2.domain.exceptions import (
    DuplicateEnrollmentException, GroupNotFoundException,
    ExpulsionDeniedException, StudentNotFoundException
)


# ==========================================
# 1. ТЕСТЫ: УЧЕБНЫЙ ПРОЦЕСС (academics.py)
# ==========================================
def test_labwork_and_subject():
    lab1 = LabWork("Лаб 1", 10.0)
    lab2 = LabWork("Лаб 2", 15.0)

    assert "Обязательная" in lab1.short_info
    lab2.make_optional()
    assert "Бонусная" in lab2.short_info

    # Проверка изменения лимитов и валидации
    lab1.update_score_limit(20.0)
    with pytest.raises(ValueError):
        lab1.update_score_limit(-5.0)

    subj = Subject("ООП", 2)
    subj.add_lab(lab1)
    subj.add_lab(lab2)

    # Проверка дубликатов и поиска
    with pytest.raises(ValueError):
        subj.add_lab(LabWork("Лаб 1"))
    with pytest.raises(ValueError):
        subj.remove_lab("Несуществующая лаба")

    assert subj.total_mandatory_labs == 1
    assert len(subj.get_mandatory_labs()) == 1
    assert subj.max_possible_score == 35.0

    subj.remove_lab("Лаб 1")
    assert len(subj._labs) == 1


# ==========================================
# 2. ТЕСТЫ: ЛЮДИ (people.py)
# ==========================================
def test_person_and_student():
    student = Student("Иван", "Иванов", "Иванович")
    assert student.full_name == "Иванов Иван Иванович"
    assert str(student) == "Иванов Иван Иванович"

    student.change_last_name("Петров")
    assert student.full_name == "Петров Иван Иванович"
    with pytest.raises(ValueError):
        student.change_last_name("")

    student.financial_debt = 100.0
    assert student.is_debtor is True

    with pytest.raises(ValueError):
        student.pay_debt(-50)

    student.pay_debt(40.0)
    assert student.financial_debt == 60.0
    student.pay_debt(1000.0)
    assert student.financial_debt == 0.0

    student.is_active = False
    with pytest.raises(ValueError):
        student.grant_scholarship()


def test_lecturer_and_employee():
    prof = Professor("Петр", "Сидоров", degree="Д.т.н.")
    prof.promote("Зав. кафедрой", salary_increase=500.0)

    with pytest.raises(ValueError):
        prof.change_salary(-100)

    prof.assign_subject("Математика")
    prof.assign_subject("Математика")
    assert prof.subjects_count == 1

    with pytest.raises(ValueError):
        prof.update_degree("")

    dean = Dean("Декан", "Деканов")
    assert "ПРИКАЗ УТВЕРЖДЕН" in dean.sign_order("Отчислить")


# ==========================================
# 3. ТЕСТЫ: СТРУКТУРА (structure.py)
# ==========================================
def test_structure_hierarchy():
    spec = Speciality("ИИ", "Искусственный интеллект")
    assert str(spec) == "[ИИ] Искусственный интеллект"

    group = AcademicGroup("101", spec, max_students=2)
    assert "Группа 101" in str(group)

    s1 = Student("А", "Б")
    s2 = Student("В", "Г")
    s3 = Student("Д", "Е")

    group.enroll_student(s1)
    with pytest.raises(DuplicateEnrollmentException):
        group.enroll_student(s1)

    group.enroll_student(s2)
    with pytest.raises(ValueError, match="переполнена"):
        group.enroll_student(s3)

    group.expel_student(s1)
    assert s1 not in group.students
    assert group.has_vacancies is True

    dept = Department("Кафедра ИТ")
    dept.assign_head("Шеф")
    assert dept.head_name == "Шеф"

    lec = Lecturer("Лектор", "Лекторов")
    dept.add_teacher(lec)
    assert dept.staff_count == 1
    dept.remove_teacher(lec)
    with pytest.raises(ValueError):
        dept.remove_teacher(lec)


def test_faculty_and_university():
    f = Faculty("ФИТиУ", "ФИТиУ")
    spec = Speciality("1", "1")
    g = AcademicGroup("101", spec)
    s = Student("Студент", "Студентов")
    g.enroll_student(s)

    f.add_group(g)
    with pytest.raises(ValueError):
        f.add_group(g)

    assert f.find_student_by_id(s.person_id) == s
    assert f.find_student_by_id("fake-id") is None
    assert f.get_total_capacity() == 30

    with pytest.raises(GroupNotFoundException):
        f.get_group_strict("999")

    u = University("БГУИР", "БГУИР")
    u.add_faculty(f)
    with pytest.raises(ValueError):
        u.add_faculty(f)

    assert u.find_faculty("ФИТиУ") == f
    assert u.find_faculty("Неизвестный") is None


# ==========================================
# 4. ТЕСТЫ: ОЦЕНКИ И УСПЕВАЕМОСТЬ (grading.py)
# ==========================================
def test_record_book():
    rb = RecordBook("u-1", "ZK-1")
    assert rb.average_score == 0.0
    assert rb.get_best_subject() == "Нет оценок"

    rb.add_grade(Grade("ООП", 9, is_exam=True))
    with pytest.raises(ValueError, match="уже стоит"):
        rb.add_grade(Grade("ООП", 10, is_exam=True))

    rb.add_grade(Grade("Физика", 3, is_exam=True))
    assert rb.average_score == 6.0

    debts = rb.get_debts()
    assert "Физика" in debts
    rb.clear_debts_for_subject("Физика")
    assert len(rb.get_debts()) == 0


def test_academic_statement_and_retake():
    stmt = AcademicStatement(Subject("S", 1), AcademicGroup("1", Speciality("1", "1")), Lecturer("L", "L"))
    assert stmt.pass_rate == 0.0

    s1, s2 = Student("A", "A"), Student("B", "B")
    stmt.add_result(s1, 10)
    stmt.add_result(s2, 2)
    assert stmt.pass_rate == 50.0

    stmt.close_statement()
    with pytest.raises(ValueError):
        stmt.add_result(s1, 5)

    sheet = RetakeSheet(s1, Subject("Math", 1), max_attempts=2)
    sheet.register_attempt(3)
    sheet.register_attempt(3)
    with pytest.raises(ValueError, match="исчерпан"):
        sheet.register_attempt(4)


# ==========================================
# 5. ТЕСТЫ: ФИНАНСЫ (finance.py)
# ==========================================
def test_bank_account():
    acc1 = BankAccount("user1", "A1")
    acc2 = BankAccount("user2", "A2")

    with pytest.raises(ValueError):
        acc1.deposit(-10)
    with pytest.raises(ValueError):
        acc1.withdraw(-10)

    acc1.deposit(100)
    with pytest.raises(ValueError):
        acc1.withdraw(1000)

    acc1.transfer_to(acc2, 40)
    with pytest.raises(ValueError):
        acc1.transfer_to(acc1, 10)


def test_tuition_contract_and_payroll():
    acc = BankAccount("1", "1")
    acc.deposit(1000)
    s = Student("S", "S")
    c = TuitionContract("C-1", s, 1000.0)

    with pytest.raises(ValueError):
        c.pay_tuition(100, acc)

    c.sign_contract()
    c.pay_tuition(100, acc)
    assert c.is_fully_paid is False
    assert c.is_overdue is True

    pay = Payroll(1, 2026)
    emp = Employee("E", "E")
    emp.salary = 100
    pay.pay_salary(emp, acc, 50)

    s.has_scholarship = False
    with pytest.raises(ValueError):
        pay.pay_scholarship(s, acc)

    s.has_scholarship = True
    pay.pay_scholarship(s, acc)

    assert pay.total_payments_count == 2
    assert len(pay.get_payment_history()) == 2


# ==========================================
# 6. ТЕСТЫ: ИНФРАСТРУКТУРА И БИБЛИОТЕКА
# ==========================================
def test_infrastructure():
    room = Room("101", capacity=1)
    s1 = Student("А", "Б")
    room.check_in(s1)

    with pytest.raises(ValueError):
        room.evict(Student("Чужой", "Студент"))

    dorm = Dormitory(1, "A")
    dorm.add_room(room)
    with pytest.raises(ValueError):
        dorm.add_room(Room("101", 2))

    assert dorm.find_room_for_student(s1) == room
    assert dorm.find_room_for_student(Student("B", "B")) is None
    assert len(dorm.get_available_rooms()) == 0
    assert dorm.occupancy_rate == 100.0


def test_library():
    book = Book("Книга", "Автор", "123", 1)
    book.borrow()
    book.return_book()
    with pytest.raises(ValueError):
        book.return_book()

    card = LibraryCard(Student("А", "Б"))
    books = [Book(str(i), "A", "1", 1) for i in range(6)]
    for b in books[:5]:
        card.take_book(b)

    with pytest.raises(ValueError):
        card.take_book(books[5])
    with pytest.raises(ValueError):
        card.return_book(books[5])

    assert card.has_book(books[0]) is True


# ==========================================
# 7. ТЕСТЫ: РАСПИСАНИЕ (schedule.py)
# ==========================================
def test_schedule():
    room = Classroom("101", 30, has_computers=False)
    room.close_for_maintenance()
    assert room.is_available is False
    room.open_classroom()
    room.remove_projector()

    ts = Timeslot(1, "10:00", "11:30")
    assert ts.duration_minutes == 90

    subj = Subject("Лаба", 1)
    l = Lecturer("L", "L")
    g = AcademicGroup("1", Speciality("1", "1"), max_students=5)

    room.equip_with_computers()
    lesson = Lesson(subj, l, g, room, ts, 1)

    tt = Timetable(1)
    tt.add_lesson(lesson)

    room.close_for_maintenance()
    lesson2 = Lesson(subj, l, g, room, ts, 2)
    with pytest.raises(ValueError):
        tt.add_lesson(lesson2)
    room.open_classroom()

    # Оверлап группы
    lesson_group = Lesson(Subject("S2", 1), Lecturer("L2", "L2"), g, Classroom("2", 10), ts, 1)
    with pytest.raises(ValueError):
        tt.add_lesson(lesson_group)

    # Оверлап препода
    lesson_lect = Lesson(Subject("S2", 1), l, AcademicGroup("2", Speciality("1", "1")), Classroom("2", 10), ts, 1)
    with pytest.raises(ValueError):
        tt.add_lesson(lesson_lect)

    assert len(tt.get_schedule_for_group("1", 1)) == 1
    assert len(tt.get_lecturer_schedule(l.person_id, 1)) == 1


# ==========================================
# 8. ТЕСТЫ: ДОКУМЕНТЫ (documents.py)
# ==========================================
def test_orders():
    s = Student("С", "С")
    dean = Dean("Д", "Д")

    # Документ
    doc = Document("Док")
    assert doc.status == "Проект"
    doc.sign(dean)
    assert doc.status == "Подписан"
    with pytest.raises(ValueError):
        doc.sign(dean)

    # Отчисление
    exp = ExpulsionOrder(s, "Долги")
    with pytest.raises(ValueError):
        exp.execute()

    # Академ
    leave = AcademicLeaveOrder(s, "Болезнь", 6)
    with pytest.raises(ValueError):
        leave.execute()
    leave.sign(dean)
    leave.execute()
    assert s.is_active is False

    # Выговор
    s.has_scholarship = True
    rep = ReprimandOrder(s, "Шум", is_strict=False)
    rep.sign(dean)
    rep.execute()
    assert s.has_scholarship is True  # Нестрогий не лишает стипендии

    # Перевод
    g1 = AcademicGroup("1", Speciality("1", "1"))
    g2 = AcademicGroup("2", Speciality("1", "1"))
    trans = TransferOrder(s, g1, g2)
    with pytest.raises(ValueError):
        trans.execute()

    # Стипендия
    schol = ScholarshipOrder([s])
    with pytest.raises(ValueError):
        schol.execute()


# ==========================================
# 9. ТЕСТЫ: ФАСАД ДЕКАНАТА (dean_office.py)
# ==========================================
@pytest.fixture
def office_setup():
    dean = Dean("Декан", "Деканов")
    fitu = Faculty("ФИТиУ", "ФИТиУ")
    group = AcademicGroup("101", Speciality("1", "1"))
    fitu.add_group(group)
    return DeanOffice(fitu, dean)


def test_dean_office_integration(office_setup):
    office = office_setup
    s1 = Student("Хорошист", "А")
    office.enroll_student(s1, "101")

    with pytest.raises(StudentNotFoundException):
        office.get_student_record_book("fake")

    # Тест перевода
    g2 = AcademicGroup("102", Speciality("2", "2"))
    office.faculty.add_group(g2)
    office.transfer_student(s1, "101", "102")
    assert s1 in g2.students
    assert s1 not in office.faculty.get_group_strict("101").students

    # Тест выговора
    office.issue_reprimand(s1, "Нарушение", is_strict=False)
    assert len(office._archive_orders) > 0


from lab2.domain.documents import AcademicCertificate, AcademicLeaveOrder, ReprimandOrder


def test_missing_coverage_people_and_structure():
    # people.py (строки 15, 25, 50, 59, 70-72, 78, 89-90, 95, 99, 104, 114)
    p = Person("Имя", "Фамилия")
    p.change_last_name("Новая")
    assert str(p) == "Новая Имя"

    s = Student("Студент", "С")
    s.financial_debt = 50.0
    s.pay_debt(100.0)  # Погашение больше долга (строка 59)
    assert s.financial_debt == 0.0

    s.is_active = True
    s.grant_scholarship()  # Назначение стипендии (строка 50)

    emp = Employee("Сотрудник", "С")
    emp.promote("Директор", 100.0)  # Повышение с ЗП (строка 70-72)
    emp.change_salary(200.0)  # Смена ЗП (строка 78)

    lec = Lecturer("Лектор", "Л")
    lec.assign_subject("Математика")  # Назначение предмета (строка 89-90)
    lec.update_degree("Доцент")  # Обновление степени (строка 95)
    assert lec.can_teach("Математика") is True  # (строка 99)
    assert lec.subjects_count == 1  # (строка 104)

    dean = Dean("Декан", "Д")
    assert "ПРИКАЗ УТВЕРЖДЕН" in dean.sign_order("Тест")  # (строка 114)

    # structure.py (строки 12, 18, 41, 44, 53, 58, 63, 67, 77, 86, 93, 108, 127, 132, 136-140)
    spec = Speciality("Код", "Имя")
    assert str(spec) == "[Код] Имя"
    spec.update_semesters_count(8)

    g = AcademicGroup("1", spec, 2)
    g.enroll_student(s)
    assert s in g.students  # (строка 41)
    assert g.is_full() is False  # (строка 44)
    assert "Группа" in str(g)  # (строка 58)
    assert len(g.active_students) == 1  # (строка 63)
    g.clear_expelled()  # (строка 67)

    dept = Department("Кафедра")
    dept.assign_head("Шеф")  # (строка 77)
    dept.add_teacher(lec)
    dept.remove_teacher(lec)  # Успешное удаление (строка 86)
    assert dept.staff_count == 0  # (строка 93)

    f = Faculty("ФАК", "Ф")
    f.add_department(dept)  # (строка 108)
    f.add_group(g)
    assert f.get_total_capacity() == 2  # (строка 127)
    assert f.find_student_by_id(s.person_id) == s  # (строки 136-140)


def test_missing_coverage_grading_finance_docs():
    # grading.py (строки 41, 58, 63-65, 71-72, 91-92, 103-104)
    rb = RecordBook("1", "1")
    rb.add_grade(Grade("ООП", 9))
    assert rb.average_score == 9.0  # (строка 41)
    assert rb.is_excellent is True  # (строка 58)
    assert rb.get_best_subject() == "ООП"  # (строки 63-65)

    stmt = AcademicStatement(Subject("S", 1), AcademicGroup("1", Speciality("1", "1")), Lecturer("L", "L"))
    stmt.add_result(Student("A", "A"), 9)
    assert stmt.pass_rate == 100.0  # (строки 91-92)

    sheet = RetakeSheet(Student("A", "A"), Subject("S", 1), 2)
    sheet.register_attempt(3)
    sheet.register_attempt(3)  # Исчерпание попыток, is_valid = False (строки 103-104)
    assert sheet.is_valid is False

    # finance.py (строки 25-29, 39-40, 56-57, 61, 65, 72-74, 80-82, 87, 101-104)
    acc1 = BankAccount("1", "1")
    acc2 = BankAccount("2", "2")
    acc1.deposit(1000)
    acc1.transfer_to(acc2, 500)  # Транзакция (строки 39-40)
    with pytest.raises(ValueError):
        acc1.withdraw(5000)  # Недостаточно средств (строки 25-29)

    s = Student("С", "С")
    s.has_scholarship = True
    c = TuitionContract("1", s, 1000)
    assert c.debt == 1000  # (строки 56-57)
    assert c.is_fully_paid is False  # (строка 61)
    assert c.is_overdue is True  # (строки 80-82)

    c.sign_contract()
    c.pay_tuition(100, acc2)  # Списание со счета (строка 65)
    c.apply_discount(10)  # Скидка (строки 72-74)

    pay = Payroll(1, 2026)  # (строка 87)
    pay.pay_scholarship(s, acc1)  # Начисление стипендии (строки 101-104)

    # documents.py (строки 28, 34-36, 59, 68-70, 121-122)
    doc = Document("Д")
    with pytest.raises(ValueError):
        doc.cancel_document("Причина")  # (строка 28)
    doc.sign(Dean("Д", "Д"))
    doc.cancel_document("Отмена")  # Аннулирование (строки 34-36)

    cert = AcademicCertificate(s, "Справка")  # (строка 59)

    g1 = AcademicGroup("1", Speciality("1", "1"))
    g2 = AcademicGroup("2", Speciality("1", "1"))
    g1.enroll_student(s)
    t = TransferOrder(s, g1, g2)
    t.sign(Dean("Д", "Д"))
    t.execute()  # Выполнение перевода (строки 68-70)

    r = ReprimandOrder(s, "Шум", is_strict=True)
    r.sign(Dean("Д", "Д"))
    r.execute()  # Лишение стипендии за строгий выговор (строки 121-122)


def test_missing_coverage_infra_library_schedule():
    # infrastructure.py (строки 22, 29, 38, 56-59, 63, 70-72)
    r = Room("1", 2)
    s = Student("С", "С")
    r.check_in(s)  # (строка 22)
    r.evict(s)  # (строка 29)
    r.check_in(s)
    r.evict_all()  # (строка 38)

    d = Dormitory(1, "1")
    d.add_room(r)
    r.check_in(s)
    assert d.find_room_for_student(s) == r  # (строки 56-59)
    assert len(d.get_available_rooms()) > 0  # (строка 63)
    assert d.occupancy_rate == 50.0  # (строки 70-72)

    # library.py (строки 17, 28, 33, 52-53, 58, 62)
    b = Book("B", "A", "1", 1)
    assert b.is_available is True  # (строка 28)
    assert b.popularity_index == 0  # (строка 33)

    card = LibraryCard(s)
    card.take_book(b)  # (строки 17, 52-53)
    assert card.borrowed_count == 1  # (строка 62)
    card.return_book(b)  # (строка 58)

    # schedule.py (строки 21, 25, 35, 49-51, 92, 107-110, 114-116)
    c = Classroom("1", 10)
    c.equip_with_computers(5)  # (строки 21, 25)
    c.remove_projector()  # (строка 35)

    subj = Subject("Лабораторная работа", 1)
    l = Lecturer("L", "L")
    g = AcademicGroup("1", Speciality("1", "1"))
    ts = Timeslot(1, "10:00", "11:00")

    c2 = Classroom("2", 10)  # Без компьютеров
    with pytest.raises(ValueError):
        Lesson(subj, l, g, c2, ts, 1)  # Ошибка оборудования (строки 49-51)

    les = Lesson(subj, l, g, c, ts, 1)
    tt = Timetable(1)
    tt.add_lesson(les)  # (строка 92)
    assert len(tt.get_schedule_for_group("1", 1)) == 1  # (строки 107-110)
    assert len(tt.get_lecturer_schedule(l.person_id, 1)) == 1  # (строки 114-116)


def test_missing_coverage_dean_office():
    # dean_office.py (строки 35, 70, 74)
    f = Faculty("Ф", "Ф")
    g1 = AcademicGroup("101", Speciality("1", "1"))
    g2 = AcademicGroup("102", Speciality("1", "1"))
    f.add_group(g1)
    f.add_group(g2)

    office = DeanOffice(f, Dean("Д", "Д"))
    s = Student("Отличник", "О")
    office.enroll_student(s, "101")

    # Инициируем перевод для покрытия строки 35
    office.transfer_student(s, "101", "102")

    # Добавляем 10 баллов и подводим итоги (покроет строки 70 и 74 - выдачу стипендии)
    rb = office.get_student_record_book(s.person_id)
    rb.add_grade(Grade("Мат", 10, is_exam=True))
    office.summarize_session()

    assert s.has_scholarship is True