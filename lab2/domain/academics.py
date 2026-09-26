import uuid


class LabWork:
    """
    Учебная лабораторная работа.

    Attributes:
        title (str): Название лабораторной работы.
        max_score (float): Максимальный балл за выполнение.
        is_mandatory (bool): Обязательна ли к сдаче для допуска к экзамену.
        lab_id (str): Уникальный внутренний идентификатор (UUID).
    """
    DEFAULT_MAX_SCORE = 10.0

    def __init__(self, title: str, max_score: float = DEFAULT_MAX_SCORE) -> None:
        self.lab_id = str(uuid.uuid4())
        self.title = title
        self.max_score = max_score
        self.is_mandatory = True

    def make_optional(self) -> None:
        """Делает лабораторную работу необязательной (бонусной)."""
        self.is_mandatory = False

    @property
    def short_info(self) -> str:
        """Агрегация: возвращает краткую информацию о статусе и баллах."""
        status = "Обязательная" if self.is_mandatory else "Бонусная"
        return f"[{status}] {self.title} (Max: {self.max_score})"

    def update_score_limit(self, new_max: float) -> None:
        """
        Корректирует максимальный балл за лабораторную работу.

        Args:
            new_max (float): Новый максимальный балл.

        Raises:
            ValueError: Если новый балл нулевой или отрицательный.
        """
        if new_max <= 0:
            raise ValueError("Максимальный балл не может быть нулевым или отрицательным.")
        self.max_score = new_max


class Subject:
    """
    Учебная дисциплина, состоящая из набора лабораторных работ.

    Attributes:
        name (str): Название дисциплины.
        semester (int): Номер семестра, в котором читается курс.
        exam_required (bool): Требуется ли сдача экзамена.
        subject_id (str): Уникальный внутренний идентификатор (UUID).
    """

    def __init__(self, name: str, semester: int, exam_required: bool = True) -> None:
        self.subject_id = str(uuid.uuid4())
        self.name = name
        self.semester = semester
        self.exam_required = exam_required
        self._labs: list[LabWork] = []

    def add_lab(self, lab: LabWork) -> None:
        """
        Добавляет новую лабораторную работу в учебный курс.

        Args:
            lab (LabWork): Экземпляр лабораторной работы.

        Raises:
            ValueError: Если лабораторная с таким названием уже существует.
        """
        if any(existing_lab.title == lab.title for existing_lab in self._labs):
            raise ValueError(f"Лабораторная '{lab.title}' уже существует в курсе {self.name}")
        self._labs.append(lab)

    def remove_lab(self, title: str) -> None:
        """
        Удаляет лабораторную работу из курса по ее названию.

        Args:
            title (str): Название удаляемой лабораторной работы.

        Raises:
            ValueError: Если лабораторная работа не найдена.
        """
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
        """
        Фильтрация: возвращает список только обязательных лабораторных работ.

        Returns:
            list[LabWork]: Список обязательных работ.
        """
        return [lab for lab in self._labs if lab.is_mandatory]