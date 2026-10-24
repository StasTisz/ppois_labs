"""Консольный интерфейс (CLI) для информационной системы университета (Лаба №2).

Обеспечивает интерактивное управление всеми доменами:
1. Структура (structure/) - добавление/удаление групп и студентов
2. Персонал (people/) - наем/увольнение профессоров, доцентов, ассистентов
3. Учебный процесс (academics/ & schedule/) - дисциплины, лабы, расписание
4. Успеваемость (grading/) - зачетки, выставление оценок, ведомости, пересдачи
5. Финансы (finance/) - оплата обучения по контрактам, зарплатный фонд
6. Инфраструктура (infrastructure/ & library/) - заселение/выселение, книги
7. Деканат (documents/ & dean_office/) - приказы, справки, итоги сессии
"""

from __future__ import annotations

import os
import pickle
import sys
from collections.abc import Callable

from lab2.domain.academics import LabWork, Subject
from lab2.domain.dean_office import DeanOffice
from lab2.domain.documents import AcademicCertificate, AcademicLeaveOrder
from lab2.domain.exceptions import DeanOfficeException
from lab2.domain.finance import BankAccount, Payroll, TuitionContract
from lab2.domain.grading import AcademicStatement, Grade, RetakeSheet
from lab2.domain.infrastructure import Dormitory, Room
from lab2.domain.library import Book, LibraryCard
from lab2.domain.people import (
    Assistant,
    AssociateProfessor,
    Dean,
    Lecturer,
    Professor,
    Student,
)
from lab2.domain.schedule import Classroom, Lesson, Timeslot, Timetable
from lab2.domain.structure import (
    AcademicGroup,
    Department,
    Faculty,
    Speciality,
    University,
)

DEFAULT_STATE_FILE = "lab2_state.pkl"


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
    """Генератор стартовых данных университета."""

    @staticmethod
    def _seed_structure() -> tuple[
        University, Faculty, DeanOffice, AcademicGroup, AcademicGroup, Department
    ]:
        uni = University("Белорусский государственный университет", "БГУИР")
        fitu = Faculty("Факультет ИТиУ", "ФИТиУ")
        uni.add_faculty(fitu)
        dept = Department("Кафедра Интеллектуальных технологий")
        fitu.add_department(dept)
        dean = Dean("Анатолий", "Навроцкий", "Александрович", degree="К.т.н.")
        office = DeanOffice(fitu, dean)
        ai_spec = Speciality("1-40 05 01", "Искусственный интеллект", 8)
        group_1 = AcademicGroup("521702", ai_spec)
        group_2 = AcademicGroup("521701", ai_spec)
        fitu.add_group(group_1)
        fitu.add_group(group_2)
        return uni, fitu, office, group_1, group_2, dept

    @staticmethod
    def _seed_people_academics(
        dept: Department, g1: AcademicGroup
    ) -> tuple[Professor, AssociateProfessor, Assistant, Subject, Timetable]:
        prof = Professor("Сергей", "Липницкий", "Федорович", degree="Д.т.н.")
        assoc = AssociateProfessor("Даниил", "Шунчевич", "Вячеславович")
        asst = Assistant("Анна", "Кузнецова", "Ивановна")
        for t in (prof, assoc, asst):
            dept.add_teacher(t)
        dept.assign_head(prof)
        subj = Subject("ООП", semester=2, exam_required=True)
        subj.add_lab(LabWork("Классы и объекты", 10.0, 1))
        subj.add_lab(LabWork("Наследование и полиморфизм", 10.0, 2))
        assoc.assign_subject(subj)
        timetable = Timetable(semester_number=2)
        room = Classroom("412-2", 30, True, True)
        slot = Timeslot(1, "08:00", "09:35")
        timetable.add_lesson(Lesson(subj, assoc, g1, room, slot, 1))
        return prof, assoc, asst, subj, timetable

    @staticmethod
    def _seed_students_finance(
        office: DeanOffice, g1: AcademicGroup, g2: AcademicGroup
    ) -> tuple[Student, Student, Dormitory, TuitionContract, Payroll, list[Book]]:
        stas = Student("Стас", "Разработчиков", record_book_number="52170201")
        petr = Student("Петр", "Лентяев", record_book_number="52170202")
        office.enroll_student(stas, g1)
        office.enroll_student(petr, g2)
        dorm = Dormitory(1, "ул. Гикало, 9")
        r1 = Room("401", 2)
        dorm.add_room(r1)
        r1.check_in(stas)
        contract = TuitionContract("Д-2026/1", petr, 3500.0)
        contract.sign_contract()
        payroll = Payroll(month=5, year=2026)
        books = [
            Book("Глубокое обучение на Python", "Шолле Ф.", "978-5-4461", 5),
            Book("Язык программирования C++", "Страуструп Б.", "978-0321", 3),
        ]
        return stas, petr, dorm, contract, payroll, books

    @staticmethod
    def seed() -> dict:
        uni, fitu, office, g1, g2, dept = DataSeeder._seed_structure()
        prof, assoc, asst, subj, tt = DataSeeder._seed_people_academics(dept, g1)
        stas, petr, dorm, cont, pay, bks = DataSeeder._seed_students_finance(office, g1, g2)
        d = {"uni": uni, "faculty": fitu, "office": office, "dept": dept, "g1": g1, "g2": g2}
        d.update({"prof": prof, "assoc": assoc, "asst": asst, "subj": subj, "timetable": tt})
        d.update({"stas": stas, "petr": petr, "dorm": dorm, "contract": cont, "payroll": pay, "books": bks})
        return d


class CLI:
    """Интерактивный консольный интерфейс управления университетом (Лаба №2)."""

    def __init__(self, state_file: str = DEFAULT_STATE_FILE) -> None:
        self.state_file = state_file
        print("Инициализация доменной модели... Загрузка данных.")
        self.state = DataSeeder.seed()
        self.office: DeanOffice = self.state["office"]
        self.faculty: Faculty = self.state["faculty"]
        self.dept: Department = self.state["dept"]

    def save_state(self) -> None:
        with open(self.state_file, "wb") as f:
            pickle.dump(self.state, f)
        print(f"💾 Состояние графа сохранено в '{self.state_file}'.")

    def load_state(self) -> bool:
        if not os.path.exists(self.state_file):
            print(f"⚠️ Файл '{self.state_file}' не найден.")
            return False
        with open(self.state_file, "rb") as f:
            self.state = pickle.load(f)
        self.office = self.state["office"]
        self.faculty = self.state["faculty"]
        self.dept = self.state["dept"]
        print(f"📂 Состояние графа восстановлено из '{self.state_file}'.")
        return True

    def _show_structure(self) -> None:
        print(f"\n🏛️ Факультет: {self.faculty.name} ({self.faculty.short_name})")
        print(f"Кафедра: {self.dept.name} (Зав: {self.dept.head_name})")
        for g in self.faculty.groups:
            print(f" └─ Группа {g.number} ({g.speciality.name}): {g.students_count} студ.")
            for s in g.students:
                status = "✅" if s.is_active else "❌ (Отчислен)"
                print(f"    ├─ {status} {s.full_name} [Зачетка: {s.record_book_number}]")

    def _add_group(self) -> None:
        num = _prompt("Номер новой группы", "521703")
        spec_name = _prompt("Специальность", "Искусственный интеллект")
        spec = Speciality("1-40 05 01", spec_name, 8)
        new_g = AcademicGroup(num, spec)
        self.faculty.add_group(new_g)
        print(f"✅ Группа {num} успешно зарегистрирована на факультете.")

    def _add_student(self) -> None:
        g_num = _prompt("Номер группы для зачисления", "521702")
        g = self.faculty.find_group(g_num)
        if not g:
            print("❌ Группа не найдена.")
            return
        fn = _prompt("Имя студента", "Иван")
        ln = _prompt("Фамилия", "Новиков")
        rb = _prompt("Номер зачетной книжки", "52170299")
        stud = Student(fn, ln, record_book_number=rb)
        self.office.enroll_student(stud, g)
        print(f"✅ Студент {stud.full_name} зачислен в группу {g.number}.")

    def _expel_student_from_group(self) -> None:
        rb = _prompt("Введите номер зачетки студента для отчисления", "52170202")
        stud = self.faculty.find_student_by_record_book(rb)
        if not stud:
            print("❌ Студент с такой зачеткой не найден.")
            return
        for g in self.faculty.groups:
            if stud in g.students:
                g.expel_student(stud)
                print(f"✅ Студент {stud.full_name} отчислен из группы {g.number}.")
                return

    def _menu_structure(self) -> None:
        while True:
            print("\n--- 🏛️ СТРУКТУРА И СТУДЕНТЫ (structure/) ---")
            print("1. Показать группы и студентов\n2. Добавить учебную группу")
            print("3. Зачислить (добавить) студента\n4. Отчислить (удалить) студента\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_structure()
            elif ch == "2":
                self._add_group()
            elif ch == "3":
                self._add_student()
            elif ch == "4":
                self._expel_student_from_group()
            elif ch == "0":
                break

    def _show_teachers(self) -> None:
        print(f"\n👥 Кафедра: {self.dept.name}")
        for t in self.dept.teachers:
            stat = "В отпуске" if t.is_on_leave else "На службе"
            print(f" └─ [{t.position}] {t.full_name} | {t.degree} | Оклад: {t.salary} BYN | {stat}")

    def _add_teacher(self) -> None:
        print("Тип должности: 1. Профессор  2. Доцент  3. Ассистент")
        t_type = _prompt("Выбор", "2")
        fn = _prompt("Имя", "Михаил")
        ln = _prompt("Фамилия", "Кулешов")
        pat = _prompt("Отчество", "Игоревич")
        teacher: Lecturer
        if t_type == "1":
            teacher = Professor(fn, ln, pat, degree="Д.т.н.")
            teacher.change_salary(3200.0)
        elif t_type == "3":
            teacher = Assistant(fn, ln, pat)
            teacher.change_salary(1500.0)
        else:
            teacher = AssociateProfessor(fn, ln, pat, degree="К.т.н.")
            teacher.change_salary(2400.0)
        self.dept.add_teacher(teacher)
        print(f"✅ Нанят преподаватель: {teacher.position} {teacher.full_name}.")

    def _remove_teacher(self) -> None:
        ln = _prompt("Фамилия преподавателя для увольнения", "Кузнецова")
        target = next((t for t in self.dept.teachers if t.last_name == ln), None)
        if not target:
            print("❌ Преподаватель с такой фамилией не найден.")
            return
        self.dept.remove_teacher(target)
        print(f"✅ Преподаватель {target.full_name} уволен с кафедры.")

    def _modify_teacher(self) -> None:
        ln = _prompt("Фамилия преподавателя", "Шунчевич")
        target = next((t for t in self.dept.teachers if t.last_name == ln), None)
        if not target:
            print("❌ Преподаватель не найден.")
            return
        print("1. Предоставить отпуск  2. Вернуть из отпуска  3. Изменить оклад")
        sub_ch = _prompt("Действие", "1")
        if sub_ch == "1":
            target.grant_leave()
            print(f"✅ Преподаватель {target.full_name} отправлен в отпуск.")
        elif sub_ch == "2":
            target.return_from_leave()
            print(f"✅ Преподаватель {target.full_name} вернулся из отпуска.")
        elif sub_ch == "3":
            sal = _prompt_float("Новый оклад", 2800.0)
            target.change_salary(sal)
            print(f"✅ Оклад обновлен: {target.salary} BYN.")

    def _menu_people(self) -> None:
        while True:
            print("\n--- 👥 ПЕРСОНАЛ И ПРЕПОДАВАТЕЛИ (people/) ---")
            print("1. Список преподавателей кафедры\n2. Нанять преподавателя (полиморфизм ППС)")
            print("3. Уволить преподавателя\n4. Управление отпуском и окладом\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_teachers()
            elif ch == "2":
                self._add_teacher()
            elif ch == "3":
                self._remove_teacher()
            elif ch == "4":
                self._modify_teacher()
            elif ch == "0":
                break

    def _show_academics(self) -> None:
        subj: Subject = self.state["subj"]
        print(f"\nДисциплина: {subj.name} (Семестр {subj.semester})")
        print(f"Лабораторных работ: {len(subj.labs)}, Макс балл: {subj.max_possible_score}")
        for lab in subj.labs:
            print(f" └─ Лаб #{lab.lab_number}: {lab.title} (макс {lab.max_score} б.)")

    def _add_lab_work(self) -> None:
        subj: Subject = self.state["subj"]
        num = len(subj.labs) + 1
        title = _prompt("Название лабораторной работы", f"Лабораторная {num}")
        score = _prompt_float("Максимальный балл", 10.0)
        lab = LabWork(title, score, lab_number=num)
        subj.add_lab(lab)
        print(f"✅ Лабораторная работа '{title}' добавлена к дисциплине {subj.name}.")

    def _remove_lab_work(self) -> None:
        subj: Subject = self.state["subj"]
        title = _prompt("Название лабораторной работы для удаления", "Классы и объекты")
        try:
            subj.remove_lab(title)
            print(f"✅ Лабораторная работа '{title}' удалена из программы.")
        except ValueError as e:
            print(f"❌ Ошибка удаления: {e}")

    def _show_schedule(self) -> None:
        g_num = _prompt("Номер группы для расписания", "521702")
        g = self.faculty.find_group(g_num)
        if not g:
            print("❌ Группа не найдена.")
            return
        lessons = self.state["timetable"].get_schedule_for_group(g, day_of_week=1)
        print(f"\nРасписание для группы {g_num} (Понедельник):")
        if not lessons:
            print(" Пар нет.")
        for l in lessons:
            print(f" └─ [{l.timeslot.start_time}-{l.timeslot.end_time}] {l.subject.name} | Ауд. {l.room.number} | Преп. {l.lecturer.last_name}")

    def _add_lesson_to_schedule(self) -> None:
        tt: Timetable = self.state["timetable"]
        g: AcademicGroup = self.state["g1"]
        subj: Subject = self.state["subj"]
        assoc: AssociateProfessor = self.state["assoc"]
        room_num = _prompt("Номер аудитории", "510-2")
        pair_num = _prompt_int("Номер пары (1-5)", 2)
        room = Classroom(room_num, 30, True, True)
        slot = Timeslot(pair_num, "09:50", "11:25")
        lesson = Lesson(subj, assoc, g, room, slot, day_of_week=1)
        tt.add_lesson(lesson)
        print(f"✅ Занятие успешно добавлено в расписание группы {g.number} на Понедельник.")

    def _menu_academics_schedule(self) -> None:
        while True:
            print("\n--- 📅 УЧЕБНЫЙ ПРОЦЕСС И РАСПИСАНИЕ (academics/ & schedule/) ---")
            print("1. Список дисциплин и лабораторных\n2. Добавить лабораторную работу")
            print("3. Удалить лабораторную работу\n4. Просмотр расписания группы")
            print("5. Добавить пару в расписание\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_academics()
            elif ch == "2":
                self._add_lab_work()
            elif ch == "3":
                self._remove_lab_work()
            elif ch == "4":
                self._show_schedule()
            elif ch == "5":
                self._add_lesson_to_schedule()
            elif ch == "0":
                break

    def _show_record_book(self) -> None:
        rb_num = _prompt("Номер зачетной книжки", "52170201")
        stud = self.faculty.find_student_by_record_book(rb_num)
        if not stud:
            print("❌ Студент не найден.")
            return
        rb = self.office.get_student_record_book(stud)
        print(f"\nЗачетка: {rb.book_number} ({stud.full_name}) | Ср. балл: {rb.average_score}")
        print(f"Отличник: {'Да' if rb.is_excellent else 'Нет'} | Долгов: {len(rb.get_debts())}")
        for g in rb.grades:
            status = "Сдан" if g.is_passed else "НЕУД"
            ex_name = g.examiner.full_name if g.examiner else "Не назначен"
            print(f" └─ {g.subject_name}: {g.score} ({status}) | Экзаменатор: {ex_name}")

    def _add_grade_direct(self) -> None:
        rb_num = _prompt("Номер зачетной книжки", "52170201")
        stud = self.faculty.find_student_by_record_book(rb_num)
        if not stud:
            print("❌ Студент не найден.")
            return
        score = _prompt_int("Оценка (0-10)", 9)
        subj: Subject = self.state["subj"]
        assoc: AssociateProfessor = self.state["assoc"]
        grade = Grade(subj, score, is_exam=True, examiner=assoc)
        rb = self.office.get_student_record_book(stud)
        rb.add_grade(grade)
        print(f"✅ Оценка {score} по предмету {subj.name} внесена в зачетку {stud.full_name}.")

    def _conduct_statement(self) -> None:
        g: AcademicGroup = self.state["g1"]
        subj: Subject = self.state["subj"]
        assoc: AssociateProfessor = self.state["assoc"]
        stmt = AcademicStatement(subj, g, assoc)
        print(f"Оформление ведомости для группы {g.number} по {subj.name}:")
        for s in g.students:
            score = _prompt_int(f"Балл для {s.full_name} (0-10)", 8)
            stmt.add_result(s, score)
        stmt.close_statement()
        print(f"✅ Ведомость успешно закрыта! Процент сдачи: {stmt.pass_rate}%.")

    def _issue_retake(self) -> None:
        stud: Student = self.state["petr"]
        subj: Subject = self.state["subj"]
        assoc: AssociateProfessor = self.state["assoc"]
        sheet = RetakeSheet(stud, subj, examiner=assoc)
        score = _prompt_int(f"Результат пересдачи для {stud.full_name} (0-10)", 7)
        grade = sheet.register_attempt(score)
        if grade.is_passed:
            rb = self.office.get_student_record_book(stud)
            rb.clear_debts_for_subject(subj)
            rb.add_grade(grade)
            print("✅ Пересдача успешна! Академическая задолженность аннулирована.")
        else:
            print(f"❌ Пересдача не сдана. Осталось попыток: {sheet.remaining_attempts}.")

    def _menu_grading(self) -> None:
        while True:
            print("\n--- 📝 УСПЕВАЕМОСТЬ И СЕССИЯ (grading/) ---")
            print("1. Посмотреть зачетку студента\n2. Выставить оценку студенту")
            print("3. Оформить экзаменационную ведомость группы\n4. Выдать бегунок на пересдачу\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_record_book()
            elif ch == "2":
                self._add_grade_direct()
            elif ch == "3":
                self._conduct_statement()
            elif ch == "4":
                self._issue_retake()
            elif ch == "0":
                break

    def _show_contract(self) -> None:
        contract: TuitionContract = self.state["contract"]
        print(f"\nДоговор: {contract.number} | Студент: {contract.student.full_name}")
        print(f"Стоимость: {contract.total_amount} BYN | Долг: {contract.debt} BYN | Просрочен: {contract.is_overdue}")

    def _pay_contract(self) -> None:
        contract: TuitionContract = self.state["contract"]
        amount = _prompt_float("Сумма к оплате (BYN)", 500.0)
        acc = BankAccount(contract.student, "BY52TEMP-ACC")
        acc.deposit(amount)
        contract.pay_tuition(amount, acc)
        print(f"✅ Платеж {amount} BYN зачислен. Остаток долга: {contract.debt} BYN.")

    def _pay_salaries(self) -> None:
        payroll: Payroll = self.state["payroll"]
        assoc: AssociateProfessor = self.state["assoc"]
        bonus = _prompt_float("Премия преподавателю (BYN)", 350.0)
        acc = BankAccount(assoc, "BY52TCHR-ACC")
        payroll.pay_salary(assoc, acc, bonus=bonus)
        print(f"✅ Зарплата переведена {assoc.full_name}. Общий фонд выплат: {payroll.total_fund} BYN.")

    def _menu_finance(self) -> None:
        while True:
            print("\n--- 💰 БУХГАЛТЕРИЯ И ФИНАНСЫ (finance/) ---")
            print("1. Просмотр договора на платное обучение\n2. Внести оплату по договору")
            print("3. Выплатить заработную плату преподавателю\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_contract()
            elif ch == "2":
                self._pay_contract()
            elif ch == "3":
                self._pay_salaries()
            elif ch == "0":
                break

    def _show_infrastructure(self) -> None:
        dorm: Dormitory = self.state["dorm"]
        print(f"\n🏢 Общежитие №{dorm.number} ({dorm.address}) | Комнат: {len(dorm.rooms)}")
        for r in dorm.rooms:
            res_names = ", ".join(s.full_name for s in r.residents) or "пусто"
            print(f" └─ Комната {r.number}: {len(r.residents)}/{r.free_beds + len(r.residents)} (Проживают: {res_names})")
        print("\n📚 Библиотечный фонд:")
        for b in self.state["books"]:
            print(f" └─ '{b.title}' ({b.author}) | Доступно экз: {b.available_copies}")

    def _check_in_dorm(self) -> None:
        rb = _prompt("Номер зачетки студента для заселения", "52170202")
        stud = self.faculty.find_student_by_record_book(rb)
        if not stud:
            print("❌ Студент не найден.")
            return
        dorm: Dormitory = self.state["dorm"]
        room = dorm.rooms[0]
        room.check_in(stud)
        print(f"✅ Студент {stud.full_name} успешно заселен в комнату {room.number}.")

    def _evict_dorm(self) -> None:
        dorm: Dormitory = self.state["dorm"]
        room = dorm.rooms[0]
        if not room.residents:
            print("⚠️ В комнате нет проживающих.")
            return
        stud = room.residents[0]
        room.evict(stud)
        print(f"✅ Студент {stud.full_name} выселен из комнаты {room.number}.")

    def _borrow_book(self) -> None:
        stud: Student = self.state["stas"]
        book: Book = self.state["books"][0]
        card = LibraryCard(stud)
        card.take_book(book)
        print(f"✅ Книга '{book.title}' выдана студенту {stud.full_name} по билету {card.card_number}.")

    def _return_book(self) -> None:
        stud: Student = self.state["stas"]
        book: Book = self.state["books"][0]
        card = LibraryCard(stud)
        card.return_book(book)
        print(f"✅ Книга '{book.title}' возвращена в библиотеку студентом {stud.full_name}.")

    def _menu_infrastructure_library(self) -> None:
        while True:
            print("\n--- 🏢 ИНФРАСТРУКТУРА И БИБЛИОТЕКА (infrastructure/ & library/) ---")
            print("1. Осмотр общежития и книг библиотеки\n2. Заселить студента в комнату")
            print("3. Выселить студента из комнаты\n4. Выдать книгу студенту")
            print("5. Вернуть книгу в библиотеку\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._show_infrastructure()
            elif ch == "2":
                self._check_in_dorm()
            elif ch == "3":
                self._evict_dorm()
            elif ch == "4":
                self._borrow_book()
            elif ch == "5":
                self._return_book()
            elif ch == "0":
                break

    def _issue_expulsion_order(self) -> None:
        stud: Student = self.state["petr"]
        reason = _prompt("Причина отчисления", "Академическая задолженность")
        self.office.expel_student_for_debts(stud, reason=reason)
        print(f"✅ Студент {stud.full_name} отчислен приказом декана. Статус активности: {stud.is_active}.")

    def _issue_leave_order(self) -> None:
        stud: Student = self.state["stas"]
        reason = _prompt("Причина отпуска", "По состоянию здоровья")
        months = _prompt_int("Срок отпуска (мес: 6, 12, 24)", 12)
        order = AcademicLeaveOrder(stud, reason, months)
        order.sign(self.office.dean)
        order.execute()
        print(f"✅ Оформлен {order.title}. Допустим: {order.is_eligible()}.")

    def _issue_certificate(self) -> None:
        stud: Student = self.state["stas"]
        dest = _prompt("Место требования", "Посольство")
        cert = AcademicCertificate(stud, destination=dest)
        print(f"✅ Выдана справка: '{cert.title}'. Статус студента валиден: {cert.verify_student_status()}.")

    def _summarize_session(self) -> None:
        self.office.summarize_session()
        debtors = self.office.get_all_debtors()
        active = self.office.total_active_students
        print("\n📊 Итоги сессии деканата:")
        print(f" └─ Всего активных студентов на факультете: {active}")
        print(f" └─ Должников на контроле: {len(debtors)}")

    def _menu_dean_office(self) -> None:
        while True:
            print("\n--- 👔 ДОКУМЕНТООБОРОТ ДЕКАНАТА (documents/ & dean_office/) ---")
            print("1. Приказ об отчислении студента\n2. Приказ на академический отпуск")
            print("3. Выдать академическую справку\n4. Подвести итоги сессии\n0. Назад")
            ch = _prompt("Выбор", "1")
            if ch == "1":
                self._issue_expulsion_order()
            elif ch == "2":
                self._issue_leave_order()
            elif ch == "3":
                self._issue_certificate()
            elif ch == "4":
                self._summarize_session()
            elif ch == "0":
                break

    def _handle_menu_choice(self, choice: str) -> None:
        actions: dict[str, Callable[[], object]] = {
            "1": self._menu_structure,
            "2": self._menu_people,
            "3": self._menu_academics_schedule,
            "4": self._menu_grading,
            "5": self._menu_finance,
            "6": self._menu_infrastructure_library,
            "7": self._menu_dean_office,
            "8": self.save_state,
            "9": self.load_state,
        }
        if choice in actions:
            actions[choice]()
        elif choice == "0":
            print("🚪 Завершение работы системы. До свидания!")
            sys.exit(0)
        else:
            print("⚠️ Неизвестная команда.")

    def _print_main_menu(self) -> None:
        print("\n" + "=" * 60)
        print("🎓 ИНФОРМАЦИОННАЯ СИСТЕМА УНИВЕРСИТЕТА (LAB 2 INTERACTIVE)")
        print("=" * 60)
        print("1. 🏛️  Структура и Студенты (structure/: добавить/удалить группы и студентов)")
        print("2. 👥 Персонал кафедры (people/: нанять/уволить профессора, доцента, ассистента)")
        print("3. 📅 Учебный процесс (academics/ & schedule/: добавить/удалить лабы, пары)")
        print("4. 📝 Успеваемость (grading/: зачетка, оценка, ведомость, бегунок)")
        print("5. 💰 Бухгалтерия (finance/: оплатить контракт, выплата зарплат)")
        print("6. 🏢 Инфраструктура (infrastructure/ & library/: заселить/выселить, книги)")
        print("7. 👔 Деканат (documents/ & dean_office/: приказы, справки, итоги)")
        print("8. 💾 Сохранить состояние в файл (Pickle State)")
        print("9. 📂 Загрузить состояние из файла (Pickle State)")
        print("0. Выход\n" + "=" * 60)

    def run(self) -> None:
        while True:
            self._print_main_menu()
            choice = input("\nВыбор > ").strip()
            try:
                self._handle_menu_choice(choice)
            except DeanOfficeException as e:
                print(f"\n❌ БИЗНЕС-ОШИБКА ДЕКАНАТА: {e}")
            except ValueError as e:
                print(f"\n⚠️ ОШИБКА ДАННЫХ: {e}")
            except Exception as e:  # noqa: BLE001
                print(f"\n🔥 КРИТИЧЕСКАЯ ОШИБКА: {e}")


def main() -> None:
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
