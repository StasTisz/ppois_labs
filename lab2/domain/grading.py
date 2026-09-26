import uuid
from datetime import datetime, timezone

from lab2.domain.academics import Subject
from lab2.domain.people import Lecturer, Student
from lab2.domain.structure import AcademicGroup


class Grade:
    """
    Оценка за конкретный вид контроля (экзамен, зачет, лабораторная).

    Attributes:
        subject_name (str): Название дисциплины.
        score (int): Выставленный балл.
        is_exam (bool): Является ли оценка итоговой (экзаменационной).
        date_issued (datetime): Точное время выставления оценки (в UTC).
    """
    MIN_SCORE = 0
    MAX_SCORE = 10
    MIN_PASSING_SCORE = 4

    def __init__(self, subject_name: str, score: int, is_exam: bool = False) -> None:
        self.subject_name = subject_name
        self.score = score
        self.is_exam = is_exam
        self.date_issued = datetime.now(timezone.utc)
        self._validate_score()

    def _validate_score(self) -> None:
        """
        Внутренний валидатор диапазона оценки.

        Raises:
            ValueError: Если балл выходит за допустимые границы (0-10).
        """
        if not (self.MIN_SCORE <= self.score <= self.MAX_SCORE):
            raise ValueError(
                f"Недопустимый балл: {self.score}. В системе оценок допустимы "
                f"значения от {self.MIN_SCORE} до {self.MAX_SCORE}."
            )

    @property
    def is_passed(self) -> bool:
        """Бизнес-правило: считается ли предмет сданным (4 балла и выше)."""
        return self.score >= self.MIN_PASSING_SCORE


class RecordBook:
    """
    Зачетная книжка конкретного студента, хранящая историю всех оценок.

    Attributes:
        student_id (str): Идентификатор владельца (Student.person_id).
        book_number (str): Уникальный номер бланка зачетной книжки.
    """

    def __init__(self, student_id: str, book_number: str) -> None:
        self.student_id = student_id
        self.book_number = book_number
        self._grades: list[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        """
        Вносит новую оценку в зачетную книжку.

        Args:
            grade (Grade): Объект выставляемой оценки.

        Raises:
            ValueError: Если экзаменационная оценка по этому предмету уже стоит.
        """
        if grade.is_exam and any(g.subject_name == grade.subject_name and g.is_exam for g in self._grades):
            raise ValueError(f"Экзаменационная оценка по {grade.subject_name} уже стоит в зачетке {self.book_number}")
        self._grades.append(grade)

    @property
    def average_score(self) -> float:
        """Агрегация: вычисляет средний балл по всем записям."""
        if not self._grades:
            return 0.0
        total = sum(g.score for g in self._grades)
        return round(total / len(self._grades), 2)

    def get_debts(self) -> list[str]:
        """
        Анализ успеваемости: формирует список предметов с академической задолженностью.

        Returns:
            list[str]: Названия несданных дисциплин.
        """
        return [grade.subject_name for grade in self._grades if not grade.is_passed]

    def clear_debts_for_subject(self, subject_name: str) -> None:
        """
        Удаляет неудовлетворительные оценки по предмету после успешной пересдачи.

        Args:
            subject_name (str): Название дисциплины, по которой закрыт долг.
        """
        self._grades = [g for g in self._grades if not (g.subject_name == subject_name and not g.is_passed)]

    @property
    def is_excellent(self) -> bool:
        """Бизнес-правило: является ли студент круглым отличником (все оценки >= 9)."""
        if not self._grades:
            return False
        return all(g.score >= 9 for g in self._grades)

    def get_best_subject(self) -> str | None:
        """
        Ищет предмет с максимальным баллом.

        Returns:
            str | None: Название предмета или None, если оценок нет.
        """
        if not self._grades:
            return None
        best_grade = max(self._grades, key=lambda g: g.score)
        return best_grade.subject_name


class AcademicStatement:
    """
    Экзаменационная ведомость группы для конкретной дисциплины.

    Attributes:
        statement_id (str): Уникальный номер ведомости.
        subject (Subject): Учебная дисциплина.
        group (AcademicGroup): Экзаменуемая группа.
        examiner (Lecturer): Преподаватель, принимающий экзамен.
        is_closed (bool): Статус документа (закрыт/открыт).
    """

    def __init__(self, subject: Subject, group: AcademicGroup, examiner: Lecturer) -> None:
        self.statement_id = str(uuid.uuid4())
        self.subject = subject
        self.group = group
        self.examiner = examiner
        self.is_closed = False
        self._results: dict[str, Grade] = {}  # Ключ: student_id, Значение: Grade

    def add_result(self, student: Student, score: int) -> None:
        """
        Вносит оценку конкретного студента в ведомость.

        Args:
            student (Student): Сдающий студент.
            score (int): Выставленный балл.

        Raises:
            ValueError: Если ведомость уже закрыта.
        """
        if self.is_closed:
            raise ValueError("Ведомость уже закрыта и передана в деканат.")

        grade = Grade(self.subject.name, score, is_exam=True)
        self._results[student.person_id] = grade

    def close_statement(self) -> None:
        """Блокирует ведомость от дальнейших изменений."""
        self.is_closed = True

    @property
    def pass_rate(self) -> float:
        """Агрегация: вычисляет процент успешной сдачи (успеваемость группы)."""
        if not self._results:
            return 0.0
        passed = sum(1 for grade in self._results.values() if grade.is_passed)
        return round((passed / len(self._results)) * 100, 2)


class RetakeSheet:
    """
    Индивидуальное направление на пересдачу («бегунок»).

    Attributes:
        sheet_id (str): Уникальный номер бланка.
        student (Student): Направляемый студент.
        subject (Subject): Дисциплина для пересдачи.
        max_attempts (int): Максимально разрешенное количество попыток.
        attempts_used (int): Использованное количество попыток.
        is_valid (bool): Действителен ли бегунок. False - 
    """
    DEFAULT_MAX_ATTEMPTS = 3

    def __init__(self, student: Student, subject: Subject, max_attempts: int = DEFAULT_MAX_ATTEMPTS) -> None:
        self.sheet_id = str(uuid.uuid4())
        self.student = student
        self.subject = subject
        self.max_attempts = max_attempts
        self.attempts_used = 0
        self.is_valid = True

    def register_attempt(self, score: int) -> Grade:
        """
        Фиксирует попытку сдать экзамен по бегунку.

        Args:
            score (int): Полученный балл.

        Returns:
            Grade: Объект итоговой оценки.

        Raises:
            ValueError: Если лимит попыток исчерпан или бегунок недействителен.
        """
        if not self.is_valid:
            raise ValueError("Бегунок просрочен или лимит попыток исчерпан.")

        self.attempts_used += 1

        if self.attempts_used >= self.max_attempts:
            self.is_valid = False

        return Grade(self.subject.name, score, is_exam=True)