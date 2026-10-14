from __future__ import annotations

import os
import pickle
import sys

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
    def seed() -> dict:
        # 1. СТРУКТУРА (structure.py, people.py)
        uni = University(
            "Белорусский государственный университет информатики и радиоэлектроники",
            "БГУИР",
        )
        fitu = Faculty("Факультет информационных технологий и управления", "ФИТиУ")
        uni.add_faculty(fitu)

        dept_iit = Department("Кафедра Интеллектуальных информационных технологий")
        fitu.add_department(dept_iit)

        dean = Dean("Анатолий", "Навроцкий", "Александрович", degree="К.т.н.")
        office = DeanOffice(fitu, dean)

        ai_spec = Speciality("1-40 05 01", "Искусственный интеллект", semesters_count=8)
        group_ai = AcademicGroup("521702", ai_spec)
        group_ai_2 = AcademicGroup("521701", ai_spec)  # Для демонстрации перевода
        fitu.add_group(group_ai)
        fitu.add_group(group_ai_2)

        # Кадры
        teacher_oop = AssociateProfessor("Даниил", "Шунчевич", "Вячеславович")
        teacher_math = Assistant("Анна", "Кузнецова", "Ивановна")
        dept_iit.add_teacher(teacher_oop)
        dept_iit.add_teacher(teacher_math)
        dept_iit.assign_head(teacher_oop)

        # 2. УЧЕБНЫЙ ПЛАН И РАСПИСАНИЕ (academics.py, schedule.py)
        subj_oop = Subject("ООП", semester=2, exam_required=True)
        subj_oop.add_lab(LabWork("Классы и объекты", max_score=10.0, lab_number=1))
        subj_oop.add_lab(
            LabWork("Наследование и полиморфизм", max_score=10.0, lab_number=2)
        )
        teacher_oop.assign_subject(subj_oop)

        room_412 = Classroom(
            "412-2", capacity=30, has_projector=True, has_computers=True
        )
        timeslot_1 = Timeslot(1, "08:00", "09:35")
        timetable = Timetable(semester_number=2)
        lesson1 = Lesson(
            subj_oop, teacher_oop, group_ai, room_412, timeslot_1, day_of_week=1
        )
        timetable.add_lesson(lesson1)

        # 3. ИНФРАСТРУКТУРА (infrastructure.py, library.py)
        dorm = Dormitory(1, "ул. Гикало, 9")
        room_1 = Room("401", capacity=2)
        dorm.add_room(room_1)

        book_py = Book("Глубокое обучение на Python", "Шолле Ф.", "978-5-4461", 5)
        book_cpp = Book("Язык программирования C++", "Страуструп Б.", "978-5-9071", 2)

        # 4. СТУДЕНТЫ (people.py)
        stas = Student("Стас", "Разработчиков", record_book_number="52170201")
        petr = Student("Петр", "Лентяев", record_book_number="52170202")
        office.enroll_student(stas, group_ai)
        office.enroll_student(petr, group_ai)

        # Общежитие и библиотека
        room_1.check_in(stas)
        stas_lib = LibraryCard(stas)
        stas_lib.take_book(book_py)

        # 5. ФИНАНСЫ (finance.py)
        BankAccount(petr, "BY52AKBB-PETR")
        BankAccount(stas, "BY52AKBB-STAS")
        acc_teacher = BankAccount(teacher_oop, "BY52AKBB-TCHR")

        contract = TuitionContract("Д-2026/1", petr, 3500.0)
        contract.sign_contract()
        payroll = Payroll(month=5, year=2026)

        # 6. УСПЕВАЕМОСТЬ (grading.py)
        # Стас - отличник, Петр - должник
        stas_rb = office.get_student_record_book(stas)
        stas_rb.add_grade(Grade(subj_oop, 9, is_exam=True, examiner=teacher_oop))

        petr_rb = office.get_student_record_book(petr)
        petr_rb.add_grade(Grade(subj_oop, 3, is_exam=True, examiner=teacher_oop))

        return {
            "uni": uni,
            "office": office,
            "dorm": dorm,
            "payroll": payroll,
            "contract": contract,
            "books": [book_py, book_cpp],
            "subj_oop": subj_oop,
            "timetable": timetable,
            "stas": stas,
            "petr": petr,
            "teacher_oop": teacher_oop,
            "acc_teacher": acc_teacher,
            "group_ai": group_ai,
            "group_ai_2": group_ai_2,
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

    def run(self) -> None:
        while True:
            self._print_main_menu()
            choice = input("\nВыбор > ").strip()

            try:
                if choice == "1":
                    self._menu_structure()
                elif choice == "2":
                    self._menu_academics()
                elif choice == "3":
                    self._menu_grading()
                elif choice == "4":
                    self._menu_finance()
                elif choice == "5":
                    self._menu_infrastructure()
                elif choice == "6":
                    self._menu_dean_office()
                elif choice == "7":
                    self.save_state()
                elif choice == "8":
                    self.load_state()
                elif choice == "0":
                    print("🚪 Завершение работы системы. До свидания!")
                    sys.exit(0)
                else:
                    print("⚠️ Неизвестная команда.")
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
        print("0. Выход")
        print("=" * 55)

    def _menu_structure(self) -> None:
        print("\n--- 🏛️ СТРУКТУРА И КАДРЫ ---")
        uni: University = self.state["uni"]
        print(f"Университет: {uni.name} ({uni.abbreviation})")

        for fac in uni.faculties:
            print(f"\nФакультет: {fac.name} ({fac.short_name})")
            print(f"Общая вместимость: {fac.get_total_capacity()} чел.")

            print("\n Кафедры:")
            for dept in fac.departments:
                print(f" └─ {dept.name} | Зав. кафедрой: {dept.head_name}")
                for t in dept.teachers:
                    print(f"    ├─ {t.position} {t.full_name} ({t.degree})")

            print("\n Учебные группы:")
            for group in fac.groups:
                print(
                    f" └─ Группа {group.number} ({group.speciality.name}) | Студентов: {group.students_count}/{group.max_students}"
                )
                for student in group.students:
                    status = "✅" if student.is_active else "❌ (Отчислен)"
                    print(f"    ├─ {status} {student.full_name}")

    def _menu_academics(self) -> None:
        print("\n--- 📅 УЧЕБНЫЙ ПРОЦЕСС И РАСПИСАНИЕ ---")
        print("1. Посмотреть расписание группы")
        print("2. Структура дисциплины (Лабораторные)")

        choice = input("Выбор > ").strip()
        if choice == "1":
            group_num = input("Введите номер группы (напр. 521702): ").strip()
            group = self.office.faculty.find_group(group_num)
            if not group:
                print("Группа не найдена.")
                return
            schedule = self.state["timetable"].get_schedule_for_group(
                group, day_of_week=1
            )
            print(f"\nРасписание на Понедельник для {group_num}:")
            if not schedule:
                print("Пар нет.")
            for lesson in schedule:
                print(
                    f"[{lesson.timeslot.start_time}-{lesson.timeslot.end_time}] "
                    f"{lesson.subject.name} | Ауд. {lesson.room.number} | Преп. {lesson.lecturer.last_name}"
                )

        elif choice == "2":
            subj: Subject = self.state["subj_oop"]
            print(f"\nДисциплина: {subj.name} | Max балл: {subj.max_possible_score}")
            for lab in subj.get_mandatory_labs():
                print(f" - {lab.short_info}")

    def _menu_grading(self) -> None:
        print("\n--- 📝 УСПЕВАЕМОСТЬ ---")
        print("1. Посмотреть зачетку студента")
        print("2. Оформить групповую ведомость (Academic Statement)")
        print("3. Выдать бегунок на пересдачу (Retake Sheet)")

        choice = input("Выбор > ").strip()
        if choice == "1":
            student = self._select_student()
            if not student:
                return
            rb = self.office.get_student_record_book(student)
            print(f"\nЗачетка: {rb.book_number} | Средний балл: {rb.average_score}")
            print(
                f"Отличник: {'Да' if rb.is_excellent else 'Нет'} | Долгов: {len(rb.get_debts())}"
            )
            for grade in rb.grades:
                print(
                    f" - {grade.subject_name}: {grade.score} ({'Сдан' if grade.is_passed else 'Неуд'})"
                )

        elif choice == "2":
            group = self.office.faculty.get_group_strict("521702")
            statement = AcademicStatement(
                self.state["subj_oop"], group, self.state["teacher_oop"]
            )
            print("Открыта ведомость. Выставляем оценки...")
            for student in group.students:
                score_str = input(f"Оценка для {student.full_name} (0-10): ").strip()
                score = int(score_str) if score_str else 8
                statement.add_result(student, score)
            statement.close_statement()
            print(f"✅ Ведомость закрыта. Успеваемость: {statement.pass_rate}%")

        elif choice == "3":
            student = self.state["petr"]  # Петр - должник
            sheet = RetakeSheet(
                student, self.state["subj_oop"], examiner=self.state["teacher_oop"]
            )
            print(
                f"\nВыдан бегунок студенту {student.full_name} по предмету {sheet.subject.name}"
            )
            score_str = input(
                "Студент пришел на пересдачу. Введите результат (0-10): "
            ).strip()
            score = int(score_str) if score_str else 7
            grade = sheet.register_attempt(score)
            if grade.is_passed:
                rb = self.office.get_student_record_book(student)
                rb.clear_debts_for_subject(sheet.subject)
                rb.add_grade(grade)
                print("✅ Пересдача успешна! Долг закрыт.")
            else:
                print(
                    f"❌ Пересдача провалена. Осталось попыток: {sheet.remaining_attempts}"
                )

    def _menu_finance(self) -> None:
        print("\n--- 💰 БУХГАЛТЕРИЯ ---")
        print("1. Статус контракта Петра (Оплата обучения)")
        print("2. Зарплатный фонд (Выплата зарплат и стипендий)")

        choice = input("Выбор > ").strip()
        if choice == "1":
            contract: TuitionContract = self.state["contract"]
            print(
                f"Договор: {contract.number} | Долг: {contract.debt} BYN | Просрочка: {'Да' if contract.is_overdue else 'Нет'}"
            )
            if contract.debt > 0:
                amount_str = input("Сумма к оплате: ").strip()
                amount = float(amount_str) if amount_str else 500.0
                acc = BankAccount(contract.student, "BY52TEMP-ACC")
                acc.deposit(amount)
                contract.pay_tuition(amount, acc)
                print("✅ Оплата зачтена.")

        elif choice == "2":
            payroll: Payroll = self.state["payroll"]
            teacher: AssociateProfessor = self.state["teacher_oop"]
            teacher.change_salary(2500.0)
            acc = self.state["acc_teacher"]

            payroll.pay_salary(teacher, acc, bonus=300.0)
            print(
                f"✅ Зарплата переведена. Общий фонд выплат за месяц: {payroll.total_fund} BYN"
            )
            print("История транзакций фонда:")
            for log in payroll.get_payment_history():
                print(f" - {log}")

    def _menu_infrastructure(self) -> None:
        print("\n--- 🏢 ИНФРАСТРУКТУРА ---")
        dorm: Dormitory = self.state["dorm"]
        print(f"Общежитие №{dorm.number} | Заполненность: {dorm.occupancy_rate}%")
        for room in dorm.rooms:
            print(
                f"Комната {room.number} | Свободно мест: {room.free_beds}/{room.capacity}"
            )
            for res in room.residents:
                print(f"  🛏️ {res.full_name} (Долг: {res.financial_debt})")

        print("\nБиблиотека:")
        for book in self.state["books"]:
            print(f" - {book.title} | На руках: {book.popularity_index} шт.")

    def _menu_dean_office(self) -> None:
        print("\n--- 👔 ДЕКАНАТ (ПРИКАЗЫ) ---")
        print("1. Подвести итоги сессии (Отчисление должников + Стипендии)")
        print("2. Перевести студента в другую группу")
        print("3. Оформить строгий выговор")
        print("4. Выдать справку об обучении")
        print("5. Архив приказов")

        choice = input("Выбор > ").strip()
        if choice == "1":
            self.office.summarize_session()
            print("✅ Итоги подведены. Проверьте архив приказов.")

        elif choice == "2":
            student = self.state["stas"]
            print(f"Оформляем перевод студента {student.full_name} из 521702 в 521701")
            self.office.transfer_student(student, "521702", "521701")
            print("✅ Приказ о переводе исполнен.")

        elif choice == "3":
            student = self.state["petr"]
            self.office.issue_reprimand(
                student, "Нарушение режима общежития", is_strict=True
            )
            print(f"✅ Строгий выговор вынесен студенту {student.full_name}.")

        elif choice == "4":
            student = self.state["stas"]
            cert = AcademicCertificate(student, "Военный комиссариат")
            cert.sign(self.office.dean)
            print(f"✅ {cert.title} выдана для предоставления в {cert.destination}.")

        elif choice == "5":
            for order in self.office.archive_orders:
                print(f"📜 [{order.status}] {order.title}")

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
