from __future__ import annotations

import uuid

from lab2.domain.academics.labwork import LabWork


class Subject:
    def __init__(self, name: str, semester: int, exam_required: bool = True) -> None:
        self.subject_id = str(uuid.uuid4())
        self.name = name
        self.semester = semester
        self.exam_required = exam_required
        self._labs: list[LabWork] = []

    def add_lab(self, lab: LabWork) -> None:
        if any(existing_lab.title == lab.title for existing_lab in self._labs):
            raise ValueError(f"Лабораторная '{lab.title}' уже существует в курсе {self.name}")
        self._labs.append(lab)
        lab.subject = self

    def remove_lab(self, title: str) -> None:
        initial_count = len(self._labs)
        self._labs = [lab for lab in self._labs if lab.title != title]
        if len(self._labs) == initial_count:
            raise ValueError(f"Лабораторная '{title}' не найдена.")

    @property
    def total_mandatory_labs(self) -> int:
        return sum(1 for lab in self._labs if lab.is_mandatory)

    @property
    def max_possible_score(self) -> float:
        return sum(lab.max_score for lab in self._labs)

    def get_mandatory_labs(self) -> list[LabWork]:
        return [lab for lab in self._labs if lab.is_mandatory]
