from typing import List, Optional
from datetime import datetime
import uuid
from lab2.domain.academics import Subject
from lab2.domain.structure import AcademicGroup
from lab2.domain.people import Lecturer, Student


class Grade:
    """Оценка за конкретный вид контроля"""

    def __init__(self, subject_name: str, score: int, is_exam: bool = False):
        self.subject_name = subject_name
        self.score = score
        self.is_exam = is_exam  # Именно экзаменационная оценка
        self.date_issued = datetime.now()
        self._validate_score()

    def _validate_score(self):
        """Академическая оценка должна быть от 0 до 10."""
        if not (0 <= self.score <= 10):
            raise ValueError(f"Недопустимый балл: {self.score}. В системе оценок допустимы значения от 0 до 10.")

    @property
    def is_passed(self) -> bool:
        """Считается ли предмет сданным (4 балла и выше)."""
        return self.score >= 4


class RecordBook:
    """Зачетная книжка конкретного студента."""

    def __init__(self, student_id: str, book_number: str):
        self.student_id = student_id
        self.book_number = book_number
        self._grades: List[Grade] = []

    def add_grade(self, grade: Grade):
        """Добавление экзаменационной оценки"""
        if grade.is_exam and any(g.subject_name == grade.subject_name and g.is_exam for g in self._grades):
            raise ValueError(f"Экзаменационная оценка по {grade.subject_name} уже стоит в зачетке {self.book_number}")
        self._grades.append(grade)

    @property
    def average_score(self) -> float:
        """Вычисление среднего балла"""
        if not self._grades:
            return 0.0
        total = sum(g.score for g in self._grades)
        return round(total / len(self._grades), 2)

    def get_debts(self) -> List[str]:
        """Список предметов на пересдачу"""
        return [grade.subject_name for grade in self._grades if not grade.is_passed]

    def clear_debts_for_subject(self, subject_name: str):
        """Удаление неудов после пересдачи"""
        self._grades = [g for g in self._grades if not (g.subject_name == subject_name and not g.is_passed)]

    @property
    def is_excellent(self) -> bool:
        """Проверка на круглого отличника (все оценки 9 и 10)."""
        if not self._grades:
            return False
        return all(g.score >= 9 for g in self._grades)

    def get_best_subject(self) -> str:
        """Поиск предмета с максимальным баллом."""
        if not self._grades:
            return "Нет оценок"
        best_grade = max(self._grades, key=lambda g: g.score)
        return best_grade.subject_name


class AcademicStatement:
    """Экзаменационная ведомость группы."""

    def __init__(self, subject: Subject, group: AcademicGroup, examiner: Lecturer):
        self.statement_id = str(uuid.uuid4())
        self.subject = subject
        self.group = group
        self.examiner = examiner
        self.is_closed = False
        self._results = {}  # Словарь: student_id -> Grade

    def add_result(self, student: Student, score: int):
        """Поведение: внесение оценки в ведомость."""
        if self.is_closed:
            raise ValueError("Ведомость уже закрыта и передана в деканат.")

        grade = Grade(self.subject.name, score, is_exam=True)
        self._results[student.person_id] = grade

    def close_statement(self):
        """Поведение: закрытие ведомости от дальнейших изменений."""
        self.is_closed = True

    @property
    def pass_rate(self) -> float:
        """Процент успешной сдачи (успеваемость группы по ведомости)."""
        if not self._results:
            return 0.0
        passed = sum(1 for grade in self._results.values() if grade.is_passed)
        return round((passed / len(self._results)) * 100, 2)


class RetakeSheet:
    """Индивидуальное направление на пересдачу (бегунок)."""

    def __init__(self, student: Student, subject: Subject, max_attempts: int = 3):
        self.sheet_id = str(uuid.uuid4())
        self.student = student
        self.subject = subject
        self.max_attempts = max_attempts
        self.attempts_used = 0
        self.is_valid = True

    def register_attempt(self, score: int) -> Grade:
        """Поведение: попытка сдать экзамен по бегунку."""
        if not self.is_valid:
            raise ValueError("Бегунок просрочен или лимит попыток исчерпан.")

        self.attempts_used += 1

        # Если попытки кончились, бегунок сгорает
        if self.attempts_used >= self.max_attempts:
            self.is_valid = False

        return Grade(self.subject.name, score, is_exam=True)