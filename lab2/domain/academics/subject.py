from __future__ import annotations

from lab2.domain.academics.labwork import LabWork


class Subject:
    def __init__(
        self,
        name: str,
        semester: int,
        exam_required: bool = True,
        code: str = "",
    ) -> None:
        self.code = code or f"SUBJ-{abs(hash((name, semester))) % 10000:04d}"
        self.name = name
        self.semester = semester
        self.exam_required = exam_required
        self._labs: list[LabWork] = []

    @property
    def labs(self) -> list[LabWork]:
        return list(self._labs)

    def add_lab(self, lab: LabWork) -> None:
        if any(existing_lab.title == lab.title for existing_lab in self._labs):
            raise ValueError(
                f"Лабораторная '{lab.title}' уже существует в курсе {self.name}"
            )
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

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"Subject(name={self.name!r}, semester={self.semester}, code={self.code!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Subject):
            return NotImplemented
        return self.name == other.name and self.semester == other.semester

    def __hash__(self) -> int:
        return hash((self.name, self.semester))
