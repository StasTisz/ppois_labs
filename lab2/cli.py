from __future__ import annotations

import os
import pickle
import sys
from collections.abc import Callable

from lab2.domain.academics import LabWork, Subject
from lab2.domain.dean_office import DeanOffice
from lab2.domain.documents import (
    AcademicCertificate,
    AcademicLeaveOrder,
    ScholarshipOrder,
)
from lab2.domain.exceptions import DeanOfficeException
from lab2.domain.finance import BankAccount, Payroll, TuitionContract
from lab2.domain.grading import AcademicStatement, Grade, RetakeSheet
from lab2.domain.infrastructure import Dormitory, Room
from lab2.domain.library import Book, LibraryCard
from lab2.domain.people import (
    Assistant,
    AssociateProfessor,
    Dean,
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


class DataSeeder:
    """Генератор масштабных стартовых данных для демонстрации всей архитектуры."""

    @staticmethod
    def _seed_structure() -> tuple[
        University, Faculty, DeanOffice, AcademicGroup, AcademicGroup, Department
    ]:
        uni = University(
            "Белорусский государственный университет информатики и радиоэлектроники",
            "БГУИР",
        )
        fitu = Faculty("Факультет информационных технологий и управления", "ФИТиУ")
        uni.add_faculty(fitu)
        dept = Department("Кафедра Интеллектуальных информационных технологий")
        fitu.add_department(dept)
        dean = Dean("Анатолий", "Навроцкий", "Александрович", degree="К.т.н.")
        office = DeanOffice(fitu, dean)
        ai_spec = Speciality("1-40 05 01", "Искусственный интеллект", semesters_count=8)
        group_1 = AcademicGroup("521702", ai_spec)
        group_2 = AcademicGroup("521701", ai_spec)
        fitu.add_group(group_1)
        fitu.add_group(group_2)
        return uni, fitu, office, group_1, group_2, dept

    @staticmethod
    def _seed_teachers(dept: Department) -> tuple[Professor, AssociateProfessor, Assistant]:
        prof = Professor("Владимир", "Головко", "Адамович", doctoral_students_count=3)
        assoc = AssociateProfessor("Даниил", "Шунчевич", "Вячеславович")
        ass = Assistant("Анна", "Кузнецова", "Ивановна", consultation_hours=6)
        dept.add_teacher(prof)
        dept.add_teacher(assoc)
        dept.add_teacher(ass)
        dept.assign_head(assoc)
        return prof, assoc, ass

    @staticmethod
    def _seed_academics(
        prof: Professor, assoc: AssociateProfessor, ass: Assistant, group: AcademicGroup
    ) -> tuple[Subject, Subject, Timetable, Classroom]:
        subj_oop = Subject("ООП", semester=2, exam_required=True)
        lab1 = LabWork("Классы и инкапсуляция", max_score=10.0, lab_number=1)
        lab2 = LabWork("Полиморфизм и иерархии", max_score=10.0, lab_number=2)
        subj_oop.add_lab(lab1)
        subj_oop.add_lab(lab2)
        subj_ai = Subject("Нейронные сети", semester=6, exam_required=True)
        assoc.assign_subject(subj_oop)
        ass.assign_subject(subj_oop)
        prof.assign_subject(subj_ai)
        room = Classroom("412-2", capacity=30, has_projector=True, has_computers=True)
        timetable = Timetable(semester_number=2)
        slot1 = Timeslot(1, "08:00", "09:35")
        timetable.add_lesson(Lesson(subj_oop, assoc, group, room, slot1, 1))
        return subj_oop, subj_ai, timetable, room

    @staticmethod
    def _seed_students_and_grading(
        office: DeanOffice, group: AcademicGroup, teacher: AssociateProfessor, subj: Subject
    ) -> tuple[Student, Student]:
        stas = Student("Стас", "Разработчиков", record_book_number="52170201")
        petr = Student("Петр", "Лентяев", record_book_number="52170202")
        office.enroll_student(stas, group)
        office.enroll_student(petr, group)
        rb_stas = office.get_student_record_book(stas)
        rb_petr = office.get_student_record_book(petr)
        rb_stas.add_grade(Grade(subj, 9, is_exam=True, examiner=teacher))
        rb_petr.add_grade(Grade(subj, 3, is_exam=True, examiner=teacher))
        return stas, petr

    @staticmethod
    def _seed_finance_and_infra(
        stas: Student, petr: Student, assoc: AssociateProfessor
    ) -> tuple[Dormitory, Room, TuitionContract, BankAccount, Payroll, list[Book]]:
        dorm = Dormitory(1, "ул. Гикало, 9")
        room = Room("401", capacity=2)
        dorm.add_room(room)
        room.check_in(stas)
        card = LibraryCard(stas)
        book_ai = Book("Глубокое обучение на Python", "Шолле Ф.", "978-5-4461", 5)
        book_cpp = Book("Язык программирования C++", "Страуструп Б.", "978-5-8459", 3)
        card.take_book(book_ai)
        BankAccount(stas, "BY52AKBB-STAS")
        acc_petr = BankAccount(petr, "BY52AKBB-PETR")
        acc_petr.deposit(5000.0)
        acc_assoc = BankAccount(assoc, "BY52AKBB-TCHR")
        contract = TuitionContract("Д-2026/1", petr, 3500.0, bank_account=acc_petr)
        contract.sign_contract()
        payroll = Payroll(month=5, year=2026)
        payroll.pay_salary(assoc, acc_assoc, bonus=350.0)
        return dorm, room, contract, acc_assoc, payroll, [book_ai, book_cpp]

    @staticmethod
    def seed() -> dict:
        uni, fitu, office, grp1, grp2, dept = DataSeeder._seed_structure()
        prof, assoc, ass = DataSeeder._seed_teachers(dept)
        subj_oop, subj_ai, timetable, room = DataSeeder._seed_academics(prof, assoc, ass, grp1)
        stas, petr = DataSeeder._seed_students_and_grading(office, grp1, assoc, subj_oop)
        dorm, room401, contract, acc_tchr, payroll, books = DataSeeder._seed_finance_and_infra(
            stas, petr, assoc
        )
        return {
            "uni": uni,
            "fitu": fitu,
            "office": office,
            "group_1": grp1,
            "group_2": grp2,
            "dept": dept,
            "prof": prof,
            "assoc": assoc,
            "ass": ass,
            "subj_oop": subj_oop,
            "subj_ai": subj_ai,
            "timetable": timetable,
            "room": room,
            "stas": stas,
            "petr": petr,
            "dorm": dorm,
            "room401": room401,
            "contract": contract,
            "acc_tchr": acc_tchr,
            "payroll": payroll,
            "books": books,
        }


class CLI:
    """Консольный интерфейс управления системой университета (Лаба №2)."""

    DEFAULT_STATE_FILE = "lab2_state.pkl"

    def __init__(self, state_file: str | None = None) -> None:
        self.state_file = state_file or self.DEFAULT_STATE_FILE
        print("Инициализация доменной модели... Загрузка данных.")
        self.state = DataSeeder.seed()
        self.office: DeanOffice = self.state["office"]

    def save_state(self, filepath: str | None = None) -> None:
        path = filepath or self.state_file
        with open(path, "wb") as f:
            pickle.dump(self.state, f)
        print(f"💾 Состояние графа объектов успешно сохранено в '{path}'.")

    def load_state(self, filepath: str | None = None) -> bool:
        path = filepath or self.state_file
        if not os.path.exists(path):
            print(f"⚠️ Файл состояния '{path}' не найден.")
            return False
        with open(path, "rb") as f:
            self.state = pickle.load(f)
        self.office = self.state["office"]
        print(f"📂 Состояние графа объектов успешно восстановлено из '{path}'.")
        return True

    def _handle_menu_choice(self, choice: str) -> None:
        actions: dict[str, Callable[[], object]] = {
            "1": self._menu_structure,
            "2": self._menu_people_polymorphism,
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

    def _print_main_menu(self) -> None:
        print("\n" + "=" * 60)
        print("🎓 ИНФОРМАЦИОННАЯ СИСТЕМА УНИВЕРСИТЕТА (LAB 2 ENTERPRISE)")
        print("=" * 60)
        print("1. 🏛️  Структура университета (structure/: вуз, факультет, группы)")
        print("2. 👥 Полиморфизм ППС (people/: профессор, доцент, ассистент)")
        print("3. 📅 Учебный процесс (academics/ & schedule/: дисциплины, сетка)")
        print("4. 📝 Успеваемость (grading/: зачетка, ведомость, бегунки)")
        print("5. 💰 Финансы (finance/: контракт, зарплаты, счета)")
        print("6. 🏢 Инфраструктура и Книги (infrastructure/ & library/)")
        print("7. 👔 Документооборот деканата (documents/ & dean_office/)")
        print("8. 💾 Сохранить состояние в файл (Pickle State)")
        print("9. 📂 Загрузить состояние из файла (Pickle State)")
        print("0. Выход\n" + "=" * 60)

    # ---------------- 1. СТРУКТУРА (structure/) ----------------
    def _print_fac_groups(self, fac: Faculty) -> None:
        print("\n Учебные группы:")
        for g in fac.groups:
            print(f" └─ Группа {g.number} ({g.speciality.name}) | Студентов: {g.students_count}")
            for s in g.students:
                status = "✅ Активен" if s.is_active else "❌ Отчислен"
                print(f"    ├─ {status} | {s.full_name} (Зачетка: {s.record_book_number})")

    def _menu_structure(self) -> None:
        uni: University = self.state["uni"]
        fac: Faculty = self.state["fitu"]
        print("\n--- 🏛️ СТРУКТУРА УНИВЕРСИТЕТА (structure/) ---")
        print(f"Вуз: {uni.name} ({uni.abbreviation})")
        print(f"Факультет: {fac.name} ({fac.short_name}) | Вместимость: {fac.get_total_capacity()}")
        print("\n Кафедры:")
        for dept in fac.departments:
            print(f" └─ {dept.name} | Зав. кафедрой: {dept.head_name}")
            for t in dept.teachers:
                print(f"    ├─ {t.position} {t.full_name} ({t.degree})")
        self._print_fac_groups(fac)

    # ---------------- 2. КАДРЫ И ПОЛИМОРФИЗМ (people/) ----------------
    def _demo_professor(self) -> None:
        prof: Professor = self.state["prof"]
        stas: Student = self.state["stas"]
        grp: AcademicGroup = self.state["group_1"]
        print(f"\n[Профессор] {prof.full_name}:")
        print(f" -> {prof.supervise_graduate(stas, 'Архитектура глубоких сверточных сетей')}")
        print(f" -> {prof.chair_defense_committee(grp)}")
        print(f" -> {prof.conduct_scientific_seminar('Современные методы машинного обучения')}")

    def _demo_associate_prof(self) -> None:
        assoc: AssociateProfessor = self.state["assoc"]
        subj: Subject = self.state["subj_oop"]
        grp: AcademicGroup = self.state["group_1"]
        stas: Student = self.state["stas"]
        print(f"\n[Доцент] {assoc.full_name}:")
        print(f" -> {assoc.conduct_lecture(subj, grp)}")
        print(f" -> {assoc.publish_paper('Методология преподавания ООП в технических вузах')}")
        print(f" -> {assoc.publish_methodology('Практикум по паттернам проектирования', 48)}")
        grade = assoc.review_coursework(stas, subj, 9)
        print(f" -> Рецензия курсового проекта: выставлен балл {grade.score}/10")

    def _demo_assistant(self) -> None:
        ass: Assistant = self.state["ass"]
        subj: Subject = self.state["subj_oop"]
        lab: LabWork = subj.labs[0]
        grp: AcademicGroup = self.state["group_1"]
        stas: Student = self.state["stas"]
        room: Classroom = self.state["room"]
        print(f"\n[Ассистент] {ass.full_name}:")
        print(f" -> Аудитория {room.number} готова: {ass.prepare_lab_equipment(room)}")
        print(f" -> {ass.conduct_lab(subj, lab, grp)}")
        score = ass.grade_labwork(stas, lab, 9.5)
        ass.record_labwork_completed()
        print(f" -> Сдача лабы '{lab.title}': выставлен балл {score}/{lab.max_score}")

    def _demo_employee_hr(self) -> None:
        ass: Assistant = self.state["ass"]
        print(f"\n[Кадровые действия над сотрудником {ass.full_name}]:")
        ass.promote("Старший преподаватель", salary_increase=250.0)
        print(f" -> Повышение в должности: '{ass.position}', оклад повышен")
        ass.grant_leave()
        print(f" -> Оформлен трудовой отпуск: статус в отпуске = {ass.is_on_leave}")
        ass.return_from_leave()
        print(f" -> Возврат из отпуска: статус в отпуске = {ass.is_on_leave}")

    def _menu_people_polymorphism(self) -> None:
        print("\n--- 👥 ПОЛИМОРФИЗМ ПРЕПОДАВАТЕЛЕЙ (people/) ---")
        self._demo_professor()
        self._demo_associate_prof()
        self._demo_assistant()
        self._demo_employee_hr()

    # ---------------- 3. УЧЕБНЫЙ ПРОЦЕСС (academics/ & schedule/) ----------------
    def _menu_academics_schedule(self) -> None:
        subj: Subject = self.state["subj_oop"]
        tt: Timetable = self.state["timetable"]
        room: Classroom = self.state["room"]
        grp: AcademicGroup = self.state["group_1"]
        print("\n--- 📅 УЧЕБНЫЙ ПРОЦЕСС И РАСПИСАНИЕ (academics/ & schedule/) ---")
        print(f"Дисциплина: {subj.name} | Семестр: {subj.semester} | Экзамен: {subj.exam_required}")
        print("Лабораторный практикум дисциплины:")
        for lab in subj.labs:
            print(f" └─ {lab.short_info}")
        print(f"\nАудиторный фонд: Ауд. {room.number} (мест: {room.capacity}, ПК: {room.has_computers})")
        schedule = tt.get_schedule_for_group(grp, day_of_week=1)
        print(f"Сетка расписания на Понедельник для группы {grp.number}:")
        for lesson in schedule:
            print(
                f" └─ [{lesson.timeslot.start_time}-{lesson.timeslot.end_time}] "
                f"{lesson.subject.name} | Ауд. {lesson.room.number} | Преп.: {lesson.lecturer.full_name}"
            )

    # ---------------- 4. УСПЕВАЕМОСТЬ (grading/) ----------------
    def _menu_grading(self) -> None:
        print("\n--- 📝 УСПЕВАЕМОСТЬ И КОНТРОЛЬ ЗНАНИЙ (grading/) ---")
        stas: Student = self.state["stas"]
        petr: Student = self.state["petr"]
        grp: AcademicGroup = self.state["group_1"]
        assoc: AssociateProfessor = self.state["assoc"]
        subj: Subject = self.state["subj_oop"]
        statement = AcademicStatement(subj, grp, assoc)
        statement.add_result(stas, 9)
        statement.add_result(petr, 4)
        statement.close_statement()
        print(f"1. Экзаменационная ведомость #{statement.statement_number}:")
        print(f" └─ Дисциплина: {subj.name} | Успеваемость: {statement.pass_rate}%")
        rb = self.office.get_student_record_book(stas)
        print(f"\n2. Зачетная книжка {stas.full_name} (#{rb.book_number}):")
        print(f" └─ Средний балл: {rb.average_score:.2f} | Отличник: {rb.is_excellent}")
        sheet = RetakeSheet(petr, subj, examiner=assoc)
        print(f"\n3. Индивидуальный бегунок на пересдачу #{sheet.sheet_number}:")
        print(f" └─ Студент: {petr.full_name} | Осталось попыток: {sheet.remaining_attempts}")
        grade = sheet.register_attempt(7)
        print(f"    ├─ Результат пересдачи: оценка {grade.score} ({'Сдан' if grade.is_passed else 'Неуд'})")

    # ---------------- 5. БУХГАЛТЕРИЯ (finance/) ----------------
    def _menu_finance(self) -> None:
        print("\n--- 💰 БУХГАЛТЕРИЯ И ФИНАНСЫ (finance/) ---")
        petr: Student = self.state["petr"]
        contract: TuitionContract = self.state["contract"]
        payroll: Payroll = self.state["payroll"]
        acc_tchr: BankAccount = self.state["acc_tchr"]
        print("1. Договор на платное обучение (TuitionContract):")
        print(
            f" └─ Номер: {contract.number} | Студент: {petr.full_name} | "
            f"Сумма: {contract.total_amount} BYN | Долг: {contract.debt} BYN"
        )
        if contract.debt > 0 and contract.bank_account:
            contract.pay_tuition(1000.0, contract.bank_account)
            print(f"    ├─ Списана оплата 1000 BYN. Остаток долга: {contract.debt} BYN")
        print("\n2. Зарплатная ведомость (Payroll):")
        print(f" └─ Период: {payroll.month}/{payroll.year} | Общий фонд: {payroll.total_fund} BYN")
        for log in payroll.get_payment_history():
            print(f"    ├─ {log}")
        print(f"\n3. Счет преподавателя: баланс = {acc_tchr.balance} BYN")

    # ---------------- 6. ИНФРАСТРУКТУРА И КНИГИ (infrastructure/ & library/) ----------------
    def _menu_infrastructure_library(self) -> None:
        print("\n--- 🏢 ИНФРАСТРУКТУРА И БИБЛИОТЕКА (infrastructure/ & library/) ---")
        dorm: Dormitory = self.state["dorm"]
        room: Room = self.state["room401"]
        stas: Student = self.state["stas"]
        petr: Student = self.state["petr"]
        books: list[Book] = self.state["books"]
        print(f"1. Общежитие №{dorm.number} ({dorm.address}):")
        print(f" └─ Заполненность: {dorm.occupancy_rate}% | Комната {room.number}: мест {room.capacity}")
        for r in room.residents:
            print(f"    ├─ Проживает: {r.full_name}")
        room.check_in(petr)
        print(f"    ├─ Заселен студент {petr.full_name}: свободных коек = {room.free_beds}")
        print("\n2. Библиотечный фонд:")
        for b in books:
            print(f" └─ '{b.title}' ({b.author}) | Популярность: {b.popularity_index}")
        card = stas.library_card or LibraryCard(stas)
        print(f"Читательский билет #{card.card_number}: книг на руках = {card.borrowed_count}")

    # ---------------- 7. ДЕКАНАТ И ПРИКАЗЫ (documents/ & dean_office/) ----------------
    def _demo_official_documents(self) -> None:
        stas: Student = self.state["stas"]
        petr: Student = self.state["petr"]
        dean: Dean = self.office.dean
        print("Выпуск полиморфных документов (documents/):")
        cert = AcademicCertificate(stas, "По месту требования")
        cert.sign(dean)
        print(f" └─ {cert.title} -> Выдана в {cert.destination} (статус: {cert.status})")
        schol = ScholarshipOrder([stas], registration_number="П-СТИП-01")
        schol.sign(dean)
        schol.execute()
        print(f" └─ {schol.title} -> Назначена стипендия {schol.monthly_amount} BYN")
        leave = AcademicLeaveOrder(petr, "По состоянию здоровья", duration_months=12)
        leave.sign(dean)
        print(f" └─ {leave.title} -> Срок: {leave.duration_months} мес. (подписан: {leave.is_signed})")

    def _menu_dean_office(self) -> None:
        print("\n--- 👔 ДЕКАНАТ И ДОКУМЕНТООБОРОТ (documents/ & dean_office/) ---")
        dean: Dean = self.office.dean
        stas: Student = self.state["stas"]
        g1: AcademicGroup = self.state["group_1"]
        g2: AcademicGroup = self.state["group_2"]
        print(f"Декан: {dean.full_name} ({dean.degree}) | Активных студентов: {self.office.total_active_students}")
        self._demo_official_documents()
        print("\nИсполнение приказов деканата:")
        self.office.issue_reprimand(self.state["petr"], "Систематические опоздания", is_strict=False)
        print(" └─ Приказ о выговоре оформлен и подшит в личное дело.")
        self.office.transfer_student(stas, g1, g2)
        print(f" └─ Студент {stas.full_name} переведен в группу {g2.number}.")
        self.office.summarize_session()
        print(" └─ Сессия подведена: автоматические приказы созданы.")
        print(f"Архив приказов деканата: {len(self.office.archive_orders)} документов")
        for ord_doc in self.office.archive_orders[-4:]:
            print(f"    ├─ [{ord_doc.status}] {ord_doc.title}")


if __name__ == "__main__":
    app = CLI()
    app.run()
