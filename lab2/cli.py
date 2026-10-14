from __future__ import annotations

import os
import pickle
import sys
from collections.abc import Callable

from lab2.domain.academics import LabWork, Subject
from lab2.domain.dean_office import DeanOffice
from lab2.domain.documents import AcademicCertificate
from lab2.domain.exceptions import DeanOfficeException
from lab2.domain.finance import BankAccount, Payroll, TuitionContract
from lab2.domain.grading import AcademicStatement, Grade, RetakeSheet
from lab2.domain.infrastructure import Dormitory, Room
from lab2.domain.library import Book, LibraryCard
from lab2.domain.people import Assistant, AssociateProfessor, Dean, Student
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
    def _seed_structure() -> tuple[University, Faculty, DeanOffice, AcademicGroup, AcademicGroup, AssociateProfessor]:
        uni = University("Белорусский государственный университет информатики и радиоэлектроники", "БГУИР")
        fitu = Faculty("Факультет информационных технологий и управления", "ФИТиУ")
        uni.add_faculty(fitu)
        dept_iit = Department("Кафедра Интеллектуальных информационных технологий")
        fitu.add_department(dept_iit)
        office = DeanOffice(fitu, Dean("Анатолий", "Навроцкий", "Александрович", degree="К.т.н."))
        ai_spec = Speciality("1-40 05 01", "Искусственный интеллект", semesters_count=8)
        group_ai = AcademicGroup("521702", ai_spec)
        group_ai_2 = AcademicGroup("521701", ai_spec)
        fitu.add_group(group_ai)
        fitu.add_group(group_ai_2)
        teacher_oop = AssociateProfessor("Даниил", "Шунчевич", "Вячеславович")
        dept_iit.add_teacher(teacher_oop)
        dept_iit.add_teacher(Assistant("Анна", "Кузнецова", "Ивановна"))
        dept_iit.assign_head(teacher_oop)
        return uni, fitu, office, group_ai, group_ai_2, teacher_oop

    @staticmethod
    def _seed_academics(teacher: AssociateProfessor, group: AcademicGroup) -> tuple[Subject, Timetable]:
        subj_oop = Subject("ООП", semester=2, exam_required=True)
        subj_oop.add_lab(LabWork("Классы и объекты", max_score=10.0, lab_number=1))
        subj_oop.add_lab(LabWork("Наследование и полиморфизм", max_score=10.0, lab_number=2))
        teacher.assign_subject(subj_oop)
        timetable = Timetable(semester_number=2)
        room = Classroom("412-2", capacity=30, has_projector=True, has_computers=True)
        timetable.add_lesson(Lesson(subj_oop, teacher, group, room, Timeslot(1, "08:00", "09:35"), 1))
        return subj_oop, timetable

    @staticmethod
    def _enroll_and_grade(
        office: DeanOffice, group: AcademicGroup, teacher: AssociateProfessor, subj: Subject
    ) -> tuple[Student, Student]:
        stas = Student("Стас", "Разработчиков", record_book_number="52170201")
        petr = Student("Петр", "Лентяев", record_book_number="52170202")
        office.enroll_student(stas, group)
        office.enroll_student(petr, group)
        office.get_student_record_book(stas).add_grade(Grade(subj, 9, is_exam=True, examiner=teacher))
        office.get_student_record_book(petr).add_grade(Grade(subj, 3, is_exam=True, examiner=teacher))
        return stas, petr

    @staticmethod
    def _seed_people_and_finance(
        office: DeanOffice, group: AcademicGroup, teacher: AssociateProfessor, subj: Subject
    ) -> tuple[Dormitory, TuitionContract, Payroll, BankAccount, list[Book], Student, Student]:
        dorm = Dormitory(1, "ул. Гикало, 9")
        room_1 = Room("401", capacity=2)
        dorm.add_room(room_1)
        stas, petr = DataSeeder._enroll_and_grade(office, group, teacher, subj)
        room_1.check_in(stas)
        book_py = Book("Глубокое обучение на Python", "Шолле Ф.", "978-5-4461", 5)
        LibraryCard(stas).take_book(book_py)
        BankAccount(petr, "BY52AKBB-PETR")
        BankAccount(stas, "BY52AKBB-STAS")
        acc_teacher = BankAccount(teacher, "BY52AKBB-TCHR")
        contract = TuitionContract("Д-2026/1", petr, 3500.0)
        contract.sign_contract()
        return dorm, contract, Payroll(month=5, year=2026), acc_teacher, [book_py, Book("C++", "Страуструп", "1", 2)], stas, petr

    @staticmethod
    def seed() -> dict:
        uni, _fitu, office, group_ai, group_ai_2, teacher_oop = DataSeeder._seed_structure()
        subj_oop, timetable = DataSeeder._seed_academics(teacher_oop, group_ai)
        dorm, contract, payroll, acc_teacher, books, stas, petr = DataSeeder._seed_people_and_finance(
            office, group_ai, teacher_oop, subj_oop
        )
        return {
            "uni": uni, "office": office, "dorm": dorm, "payroll": payroll,
            "contract": contract, "books": books, "subj_oop": subj_oop,
            "timetable": timetable, "stas": stas, "petr": petr,
            "teacher_oop": teacher_oop, "acc_teacher": acc_teacher,
            "group_ai": group_ai, "group_ai_2": group_ai_2,
        }


class CLI:
    """Консольный интерфейс управления системой университета."""

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
            "2": self._menu_academics,
            "3": self._menu_grading,
            "4": self._menu_finance,
            "5": self._menu_infrastructure,
            "6": self._menu_dean_office,
            "7": self.save_state,
            "8": self.load_state,
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
                print(f"\n❌ БИЗНЕС-ОШИБКА: {e}")
            except ValueError as e:
                print(f"\n⚠️ ОШИБКА ВВОДА: {e}")
            except Exception as e:  # noqa: BLE001
                print(f"\n🔥 КРИТИЧЕСКАЯ ОШИБКА: {e}")

    def _print_main_menu(self) -> None:
        print("\n" + "=" * 55)
        print("🎓 ИНФОРМАЦИОННАЯ СИСТЕМА УНИВЕРСИТЕТА")
        print("=" * 55)
        print("1. 🏛️  Структура и Кадры (Университет, Кафедры)")
        print("2. 📅 Учебный процесс (Дисциплины, Расписание)")
        print("3. 📝 Успеваемость (Ведомости, Бегунки, Оценки)")
        print("4. 💰 Бухгалтерия (Контракты, Зарплаты, Стипендии)")
        print("5. 🏢 Инфраструктура (Общежитие, Библиотека)")
        print("6. 👔 Деканат (Приказы, Отчисления, Справки)")
        print("7. 💾 Сохранить состояние в файл (Pickle State)")
        print("8. 📂 Загрузить состояние из файла (Pickle State)")
        print("0. Выход\n" + "=" * 55)

    def _print_fac_info(self, fac: Faculty) -> None:
        print(f"\nФакультет: {fac.name} ({fac.short_name}) | Вместимость: {fac.get_total_capacity()} чел.")
        print("\n Кафедры:")
        for dept in fac.departments:
            print(f" └─ {dept.name} | Зав. кафедрой: {dept.head_name}")
            for teacher in dept.teachers:
                print(f"    ├─ {teacher.position} {teacher.full_name} ({teacher.degree})")
        print("\n Учебные группы:")
        for group in fac.groups:
            print(f" └─ Группа {group.number} ({group.speciality.name}) | Студентов: {group.students_count}")
            for student in group.students:
                status = "✅" if student.is_active else "❌ (Отчислен)"
                print(f"    ├─ {status} {student.full_name}")

    def _menu_structure(self) -> None:
        print("\n--- 🏛️ СТРУКТУРА И КАДРЫ ---")
        uni: University = self.state["uni"]
        print(f"Университет: {uni.name} ({uni.abbreviation})")
        for fac in uni.faculties:
            self._print_fac_info(fac)

    def _show_schedule(self) -> None:
        group_num = input("Введите номер группы (напр. 521702): ").strip()
        group = self.office.faculty.find_group(group_num)
        if not group:
            print("Группа не найдена.")
            return
        schedule = self.state["timetable"].get_schedule_for_group(group, day_of_week=1)
        print(f"\nРасписание на Понедельник для {group_num}:")
        if not schedule:
            print("Пар нет.")
        for lesson in schedule:
            print(f"[{lesson.timeslot.start_time}-{lesson.timeslot.end_time}] {lesson.subject.name} | {lesson.room.number} | {lesson.lecturer.last_name}")

    def _show_subject_labs(self) -> None:
        subj: Subject = self.state["subj_oop"]
        print(f"\nДисциплина: {subj.name} | Max балл: {subj.max_possible_score}")
        for lab in subj.get_mandatory_labs():
            print(f" - {lab.short_info}")

    def _menu_academics(self) -> None:
        print("\n--- 📅 УЧЕБНЫЙ ПРОЦЕСС И РАСПИСАНИЕ ---")
        print("1. Посмотреть расписание группы\n2. Структура дисциплины (Лабораторные)")
        choice = input("Выбор > ").strip()
        if choice == "1":
            self._show_schedule()
        elif choice == "2":
            self._show_subject_labs()

    def _show_record_book(self) -> None:
        student = self._select_student()
        if not student:
            return
        rb = self.office.get_student_record_book(student)
        print(f"\nЗачетка: {rb.book_number} | Средний балл: {rb.average_score}")
        print(f"Отличник: {'Да' if rb.is_excellent else 'Нет'} | Долгов: {len(rb.get_debts())}")
        for grade in rb.grades:
            print(f" - {grade.subject_name}: {grade.score} ({'Сдан' if grade.is_passed else 'Неуд'})")

    def _fill_statement(self) -> None:
        group = self.office.faculty.get_group_strict("521702")
        statement = AcademicStatement(self.state["subj_oop"], group, self.state["teacher_oop"])
        print("Открыта ведомость. Выставляем оценки...")
        for student in group.students:
            score_str = input(f"Оценка для {student.full_name} (0-10): ").strip()
            score = int(score_str) if score_str else 8
            statement.add_result(student, score)
        statement.close_statement()
        print(f"✅ Ведомость закрыта. Успеваемость: {statement.pass_rate}%")

    def _process_retake(self) -> None:
        student = self.state["petr"]
        sheet = RetakeSheet(student, self.state["subj_oop"], examiner=self.state["teacher_oop"])
        print(f"\nВыдан бегунок студенту {student.full_name} по предмету {sheet.subject.name}")
        score_str = input("Студент пришел на пересдачу. Введите результат (0-10): ").strip()
        score = int(score_str) if score_str else 7
        grade = sheet.register_attempt(score)
        if grade.is_passed:
            rb = self.office.get_student_record_book(student)
            rb.clear_debts_for_subject(sheet.subject)
            rb.add_grade(grade)
            print("✅ Пересдача успешна! Долг закрыт.")
        else:
            print(f"❌ Пересдача провалена. Осталось попыток: {sheet.remaining_attempts}")

    def _menu_grading(self) -> None:
        print("\n--- 📝 УСПЕВАЕМОСТЬ ---")
        print("1. Посмотреть зачетку студента\n2. Оформить групповую ведомость\n3. Выдать бегунок на пересдачу")
        choice = input("Выбор > ").strip()
        if choice == "1":
            self._show_record_book()
        elif choice == "2":
            self._fill_statement()
        elif choice == "3":
            self._process_retake()

    def _pay_contract(self) -> None:
        contract: TuitionContract = self.state["contract"]
        print(f"Договор: {contract.number} | Долг: {contract.debt} BYN | Просрочка: {'Да' if contract.is_overdue else 'Нет'}")
        if contract.debt > 0:
            amount_str = input("Сумма к оплате: ").strip()
            amount = float(amount_str) if amount_str else 500.0
            acc = BankAccount(contract.student, "BY52TEMP-ACC")
            acc.deposit(amount)
            contract.pay_tuition(amount, acc)
            print("✅ Оплата зачтена.")

    def _pay_salaries(self) -> None:
        payroll: Payroll = self.state["payroll"]
        teacher: AssociateProfessor = self.state["teacher_oop"]
        teacher.change_salary(2500.0)
        acc = self.state["acc_teacher"]
        payroll.pay_salary(teacher, acc, bonus=300.0)
        print(f"✅ Зарплата переведена. Общий фонд: {payroll.total_fund} BYN")
        for log in payroll.get_payment_history():
            print(f" - {log}")

    def _menu_finance(self) -> None:
        print("\n--- 💰 БУХГАЛТЕРИЯ ---")
        print("1. Статус контракта Петра (Оплата обучения)\n2. Зарплатный фонд (Выплата зарплат и стипендий)")
        choice = input("Выбор > ").strip()
        if choice == "1":
            self._pay_contract()
        elif choice == "2":
            self._pay_salaries()

    def _menu_infrastructure(self) -> None:
        print("\n--- 🏢 ИНФРАСТРУКТУРА ---")
        dorm: Dormitory = self.state["dorm"]
        print(f"Общежитие №{dorm.number} | Заполненность: {dorm.occupancy_rate}%")
        for room in dorm.rooms:
            print(f"Комната {room.number} | Свободно мест: {room.free_beds}/{room.capacity}")
            for res in room.residents:
                print(f"  🛏️ {res.full_name} (Долг: {res.financial_debt})")
        print("\nБиблиотека:")
        for book in self.state["books"]:
            print(f" - {book.title} | На руках: {book.popularity_index} шт.")

    def _order_summarize(self) -> None:
        self.office.summarize_session()
        print("✅ Итоги подведены. Проверьте архив приказов.")

    def _order_transfer(self) -> None:
        student = self.state["stas"]
        print(f"Оформляем перевод студента {student.full_name} из 521702 в 521701")
        self.office.transfer_student(student, self.state["group_ai"], self.state["group_ai_2"])
        print("✅ Приказ о переводе исполнен.")

    def _order_reprimand(self) -> None:
        student = self.state["petr"]
        self.office.issue_reprimand(student, "Нарушение режима общежития", is_strict=True)
        print(f"✅ Строгий выговор вынесен студенту {student.full_name}.")

    def _order_certificate(self) -> None:
        student = self.state["stas"]
        cert = AcademicCertificate(student, "Военный комиссариат")
        cert.sign(self.office.dean)
        print(f"✅ {cert.title} выдана для предоставления в {cert.destination}.")

    def _order_archive(self) -> None:
        for order in self.office.archive_orders:
            print(f"📜 [{order.status}] {order.title}")

    def _dispatch_dean_choice(self, choice: str) -> None:
        dean_actions = {
            "1": self._order_summarize,
            "2": self._order_transfer,
            "3": self._order_reprimand,
            "4": self._order_certificate,
            "5": self._order_archive,
        }
        if choice in dean_actions:
            dean_actions[choice]()

    def _menu_dean_office(self) -> None:
        print("\n--- 👔 ДЕКАНАТ (ПРИКАЗЫ) ---")
        print("1. Итоги сессии\n2. Перевод студента\n3. Выговор\n4. Справка\n5. Архив приказов")
        choice = input("Выбор > ").strip()
        self._dispatch_dean_choice(choice)

    def _select_student(self) -> Student | None:
        group_num = input("Номер группы (например, 521702): ").strip()
        group = self.office.faculty.find_group(group_num)
        if not group:
            print("Группа не найдена.")
            return None
        for i, s in enumerate(group.students):
            print(f"{i}. {s.full_name}")
        try:
            return group.students[int(input("Номер студента > "))]
        except (ValueError, IndexError):
            print("Ошибка выбора.")
            return None


if __name__ == "__main__":
    app = CLI()
    app.run()
