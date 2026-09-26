import uuid


class LabWork:
    def __init__(self, title: str, max_score: float = 10.0):
        self.lab_id = str(uuid.uuid4())
        self.title = title
        self.max_score = max_score
        self.is_mandatory = True  # Обязательна ли к сдаче для допуска к экзамену

    def make_optional(self):
        self.is_mandatory = False

    @property
    def short_info(self) -> str:
        status = "Обязательная" if self.is_mandatory else "Бонусная"
        return f"[{status}] {self.title} (Max: {self.max_score})"

    def update_score_limit(self, new_max: float):
        """Корректировка сложности лабораторной."""
        if new_max <= 0:
            raise ValueError("Максимальный балл не может быть нулевым или отрицательным.")
        self.max_score = new_max


class Subject:
    """Учебная дисциплина"""

    def __init__(self, name: str, semester: int, exam_required: bool = True):
        self.subject_id = str(uuid.uuid4())
        self.name = name
        self.semester = semester
        self.exam_required = exam_required
        self._labs: list[LabWork] = []

    def add_lab(self, lab: LabWork):
        if any(existing_lab.title == lab.title for existing_lab in self._labs):
            raise ValueError(f"Лабораторная '{lab.title}' уже существует в курсе {self.name}")
        self._labs.append(lab)

    def remove_lab(self, title: str):
        initial_count = len(self._labs)
        self._labs = [lab for lab in self._labs if lab.title != title]
        if len(self._labs) == initial_count:
            raise ValueError(f"Лабораторная '{title}' не найдена.")

    @property
    def total_mandatory_labs(self) -> int:
        return sum(1 for lab in self._labs if lab.is_mandatory)

    @property
    def max_possible_score(self) -> float:
        """Подсчет максимального балла, который можно набрать за семестр."""
        return sum(lab.max_score for lab in self._labs)

    def get_mandatory_labs(self) -> list:
        """Фильтрация: возвращает только обязательные лабы."""
        return [lab for lab in self._labs if lab.is_mandatory]