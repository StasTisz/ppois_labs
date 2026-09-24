import sys
from datetime import datetime

# Импорты всех подсистем нашей архитектуры
from lab2.domain.structure import Faculty, Speciality, AcademicGroup, Department
from lab2.domain.people import Dean, Student, AssociateProfessor, Assistant
from lab2.domain.academics import Subject, LabWork
from lab2.domain.grading import Grade
from lab2.domain.infrastructure import Dormitory, Room
from lab2.domain.finance import BankAccount, TuitionContract, Payroll
from lab2.domain.library import Book, LibraryCard
from lab2.domain.dean_office import DeanOffice
from lab2.domain.exceptions import DeanOfficeException


class DataSeeder:
    """Генератор стартовых данных для демонстрации на защите."""

    @staticmethod
    def seed() -> tuple:
        # 1. Структура и Кадры
        dean = Dean("Александр", "Иванов", "Петрович", degree="Д.т.н.")
        fitu = Faculty("Факультет информационных технологий и управления", "ФИТиУ")
        office = DeanOffice(fitu, dean)

        ai_spec = Speciality("ИИ-101", "Искусственный интеллект", semesters_count=8)
        se_spec = Speciality("ПО-201", "Программная инженерия", semesters_count=8)

        group_ai = AcademicGroup("252001", ai_spec)
        group_se = AcademicGroup("252002", se_spec)
        fitu.add_group(group_ai)
        fitu.add_group(group_se)

        teacher_oop = AssociateProfessor("Иван", "Смирнов", "Ильич")
        teacher_math = Assistant("Анна", "Кузнецова", "Ивановна")
        teacher_oop.assign_subject("ООП")
        teacher_math.assign_subject("Высшая математика")

        # 2. Инфраструктура и Библиотека
        dorm = Dormitory(1, "ул. Гикало, 9")
        room_1 = Room("401", capacity=2)
        room_2 = Room("402", capacity=3)
        dorm.add_room(room_1)
        dorm.add_room(room_2)

        book_py = Book("Глубокое обучение на Python", "Шолле Ф.", "978-5-4461", 5)
        book_cpp = Book("Язык программирования C++", "Страуструп Б.", "978-5-9071", 2)

        # 3. Студенты и Финансы
        stas = Student("Стас", "Разработчиков", record_book_number="25200101")
        petr = Student("Петр", "Лентяев", record_book_number="25200102")
        elena = Student("Елена", "Отличникова", record_book_number="25200201")

        office.enroll_student(stas, "252001")
        office.enroll_student(petr, "252001")
        office.enroll_student(elena, "252002")

        # Назначаем платное обучение Петру
        petr_account = BankAccount(petr.person_id, "BY52AKBB1234")
        contract = TuitionContract("Д-2026/1", petr, 3500.0)
        contract.sign_contract()

        # Заселяем в общежитие
        room_1.check_in(stas)
        room_1.check_in(petr)

        # Выдаем книги
        stas_lib = LibraryCard(stas)
        stas_lib.take_book(book_py)

        # Оценки (Петр — должник, Елена — отличница, Стас — хорошист)
        petr_rb = office.get_student_record_book(petr.person_id)
        petr_rb.add_grade(Grade("ООП", 3, is_exam=True))
        petr_rb.add_grade(Grade("Высшая математика", 2, is_exam=True))
        petr_rb.add_grade(Grade("Физика", 3, is_exam=True))

        elena_rb = office.get_student_record_book(elena.person_id)
        elena_rb.add_grade(Grade("ООП", 10, is_exam=True))
        elena_rb.add_grade(Grade("Высшая математика", 9, is_exam=True))

        stas_rb = office.get_student_record_book(stas.person_id)
        stas_rb.add_grade(Grade("ООП", 8, is_exam=True))
        stas_rb.add_grade(Grade("Высшая математика", 7, is_exam=True))

        return office, dorm, contract, stas_lib, [book_py, book_cpp]


class CLI:
    """Консольный интерфейс управления системой деканата."""

    def __init__(self):
        print("Загрузка среды выполнения... Пожалуйста, подождите.")
        self.office, self.dorm, self.petr_contract, self.stas_lib, self.books = DataSeeder.seed()

    def run(self):
        while True:
            self._print_main_menu()
            choice = input("\nВыбор > ").strip()

            try:
                if choice == "1":
                    self._menu_academics()
                elif choice == "2":
                    self._menu_finance()
                elif choice == "3":
                    self._menu_infrastructure()
                elif choice == "4":
                    self._menu_dean_office()
                elif choice == "0":
                    print("🚪 Завершение работы. До свидания!")
                    sys.exit(0)
                else:
                    print("⚠️ Неизвестная команда. Повторите ввод.")
            except DeanOfficeException as e:
                print(f"\n❌ БИЗНЕС-ОШИБКА: {e}")
            except ValueError as e:
                print(f"\n⚠️ ОШИБКА ВВОДА: {e}")
            except Exception as e:
                print(f"\n🔥 КРИТИЧЕСКАЯ ОШИБКА: {e}")

    # --- ГЛАВНОЕ МЕНЮ ---
    def _print_main_menu(self):
        print("\n" + "=" * 50)
        print("🎓 ИНФОРМАЦИОННАЯ СИСТЕМА ДЕКАНАТА v2.0")
        print("=" * 50)
        print("1. 📚 Учебный процесс (Оценки, Зачетки)")
        print("2. 💰 Бухгалтерия (Оплата, Долги)")
        print("3. 🏢 Инфраструктура (Общежитие, Библиотека)")
        print("4. 👔 Деканат (Отчисление, Стипендии, Приказы)")
        print("0. Выход")
        print("=" * 50)

    # --- МЕНЮ 1: УЧЕБНЫЙ ПРОЦЕСС ---
    def _menu_academics(self):
        print("\n--- 📚 УЧЕБНЫЙ ПРОЦЕСС ---")
        print("1. Посмотреть успеваемость студента")
        print("2. Выставить экзаменационную оценку")

        choice = input("Выбор > ").strip()
        if choice == "1":
            student = self._select_student()
            if not student: return
            rb = self.office.get_student_record_book(student.person_id)
            print(f"\nЗачетная книжка: {rb.book_number} | Студент: {student.full_name}")
            print(f"Средний балл: {rb.average_score}")
            print(f"Академические долги: {len(rb.get_debts())}")
            print("Оценки:")
            for grade in rb._grades:
                status = "✅ Сдан" if grade.is_passed else "❌ Неуд"
                print(f" - {grade.subject_name}: {grade.score} балл(ов) [{status}]")

        elif choice == "2":
            student = self._select_student()
            if not student: return
            subject = input("Введите название дисциплины: ")
            score = int(input("Введите оценку (0-10): "))

            rb = self.office.get_student_record_book(student.person_id)
            rb.add_grade(Grade(subject, score, is_exam=True))
            print(f"✅ Оценка успешно выставлена.")

    # --- МЕНЮ 2: БУХГАЛТЕРИЯ ---
    def _menu_finance(self):
        print("\n--- 💰 БУХГАЛТЕРИЯ ---")
        print("1. Проверить финансовые задолженности")
        print("2. Оплатить обучение (тестовый контракт Петра)")

        choice = input("Выбор > ").strip()
        if choice == "1":
            debtors = [s for g in self.office.faculty.groups for s in g.students if s.is_debtor]
            if not debtors:
                print("Финансовых должников на факультете нет.")
            else:
                for d in debtors:
                    print(f" - {d.full_name} | Долг: {d.financial_debt} BYN")

        elif choice == "2":
            print(f"Договор {self.petr_contract.number} | Студент: {self.petr_contract.student.full_name}")
            print(f"К оплате: {self.petr_contract.debt} BYN")
            amount = float(input("Сумма платежа: "))

            # Создаем временный счет для оплаты
            temp_acc = BankAccount(self.petr_contract.student.person_id, "TEST-ACC")
            temp_acc.deposit(amount + 100)  # Даем денег с запасом
            self.petr_contract.pay_tuition(amount, temp_acc)
            print(f"✅ Оплата прошла. Остаток долга: {self.petr_contract.debt} BYN")

    # --- МЕНЮ 3: ИНФРАСТРУКТУРА ---
    def _menu_infrastructure(self):
        print("\n--- 🏢 ИНФРАСТРУКТУРА ---")
        print("1. Состояние общежития")
        print("2. Библиотечный фонд")

        choice = input("Выбор > ").strip()
        if choice == "1":
            print(f"\nОбщежитие №{self.dorm.number} ({self.dorm.address})")
            print(f"Заполненность: {self.dorm.occupancy_rate}%")
            for room in self.dorm._rooms:
                status = "ПОЛОН" if room.free_beds == 0 else f"Свободно: {room.free_beds}"
                print(f"Комната {room.number} | Мест: {room.capacity} | {status}")
                for res in room._residents:
                    print(f"  🛋️ {res.full_name}")

        elif choice == "2":
            print("\nФонд библиотеки:")
            for book in self.books:
                print(f" - '{book.title}' ({book.author}) | Доступно: {book.available_copies}/{book.total_copies}")
            print(f"\nНа руках у Стаса: {self.stas_lib.borrowed_count} книг(и).")

    # --- МЕНЮ 4: ДЕКАНАТ ---
    def _menu_dean_office(self):
        print("\n--- 👔 ДЕКАНАТ ---")
        print("1. Список студентов факультета")
        print("2. Подвести итоги сессии (Авто-отчисление и Стипендии)")
        print("3. Архив изданных приказов")

        choice = input("Выбор > ").strip()
        if choice == "1":
            print(f"\nФакультет: {self.office.faculty.name}")
            for group in self.office.faculty.groups:
                print(f"\n{group.number} ({group.speciality.name}):")
                for student in group.students:
                    active = "✅" if student.is_active else "❌ (Отчислен)"
                    schol = "💰" if student.has_scholarship else ""
                    print(f" {active} {student.full_name} {schol}")

        elif choice == "2":
            print("\n⏳ Запуск процесса подведения итогов сессии...")
            self.office.summarize_session()
            print("✅ Итоги подведены! Проверьте список студентов (отчислен Петр) и приказы.")

        elif choice == "3":
            print("\nАрхив приказов деканата:")
            if not self.office._archive_orders:
                print("Архив пуст.")
            for order in self.office._archive_orders:
                print(f" 📜 [{order.created_at.strftime('%d.%m.%Y')}] {order.title} - {order.status}")

    # --- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ---
    def _select_student(self) -> Student:
        """Хелпер для выбора студента из списка."""
        group_num = input("Введите номер группы: ")
        group = self.office.faculty.find_group(group_num)
        if not group:
            print(f"Группа {group_num} не найдена.")
            return None

        print("Студенты:")
        for i, s in enumerate(group.students):
            print(f"{i}. {s.full_name}")

        try:
            idx = int(input("Номер студента > "))
            return group.students[idx]
        except (ValueError, IndexError):
            print("Неверный номер.")
            return None


if __name__ == "__main__":
    app = CLI()
    app.run()