"""Модуль учебной дисциплины кафедры."""

from __future__ import annotations

from lab2.domain.academics.labwork import LabWork


class Subject:
    """Учебная дисциплина, состоящая из набора лабораторных работ."""

    def __init__(
        self,
        name: str,
        semester: int,
        exam_required: bool = True,
        code: str = "",
    ) -> None:
        """Инициализирует экземпляр класса Subject."""
        self.code = code or f"SUBJ-{abs(hash((name, semester))) % 10000:04d}"
        self.name = name
        self.semester = semester
        self.exam_required = exam_required
        self._labs: list[LabWork] = []

    @property
    def labs(self) -> list[LabWork]:
        """Возвращает значение атрибута labs."""
        return list(self._labs)

    def add_lab(self, lab: LabWork) -> None:
        """Добавляет новую лабораторную работу в учебный курс."""
        if any(existing_lab.title == lab.title for existing_lab in self._labs):
            raise ValueError(
                f"Лабораторная '{lab.title}' уже существует в курсе {self.name}"
            )
        self._labs.append(lab)
        lab.subject = self

    def remove_lab(self, title: str) -> None:
        """Удаляет лабораторную работу из курса по ее названию."""
        initial_count = len(self._labs)
        self._labs = [lab for lab in self._labs if lab.title != title]
        if len(self._labs) == initial_count:
            raise ValueError(f"Лабораторная '{title}' не найдена.")

    @property
    def total_mandatory_labs(self) -> int:
        """Агрегация: подсчитывает количество обязательных к сдаче работ."""
        return sum(1 for lab in self._labs if lab.is_mandatory)

    @property
    def max_possible_score(self) -> float:
        """Агрегация: подсчитывает максимальный суммарный балл, который можно набрать."""
        return sum(lab.max_score for lab in self._labs)

    def get_mandatory_labs(self) -> list[LabWork]:
        """Фильтрация: возвращает список только обязательных лабораторных работ."""
        return [lab for lab in self._labs if lab.is_mandatory]

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return self.name

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return (
            f"Subject(name={self.name!r}, semester={self.semester}, code={self.code!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Subject):
            return NotImplemented
        return self.name == other.name and self.semester == other.semester

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash((self.name, self.semester))
