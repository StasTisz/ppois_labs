from lab2.domain.people import Student


class Room:
    """
    Жилая комната (блок) в общежитии.

    Attributes:
        number (str): Номер комнаты.
        capacity (int): Максимальная вместимость (количество спальных мест).
    """
    DEFAULT_CAPACITY = 4

    def __init__(self, number: str, capacity: int = DEFAULT_CAPACITY) -> None:
        self.number = number
        self.capacity = capacity
        self._residents: list[Student] = []

    @property
    def free_beds(self) -> int:
        """Агрегация: вычисляет количество свободных мест в комнате."""
        return self.capacity - len(self._residents)

    def check_in(self, student: Student) -> None:
        """
        Заселяет студента в комнату.

        Args:
            student (Student): Студент для заселения.

        Raises:
            ValueError: Если комната полностью укомплектована или студент уже заселен.
        """
        if self.free_beds <= 0:
            raise ValueError(f"Блок {self.number} полностью укомплектован.")
        if self.has_resident(student):
            raise ValueError(f"Студент {student.full_name} уже прописан в этой комнате.")
        self._residents.append(student)

    def evict(self, student: Student) -> None:
        """
        Выселяет студента из комнаты.

        Args:
            student (Student): Студент для выселения.

        Raises:
            ValueError: Если студент не проживает в этой комнате.
        """
        if not self.has_resident(student):
            raise ValueError("Студент здесь не проживает.")
        self._residents.remove(student)

    def has_resident(self, student: Student) -> bool:
        """
        Проверяет, проживает ли конкретный студент в этой комнате.

        Args:
            student (Student): Искомый студент.

        Returns:
            bool: True, если студент числится в комнате, иначе False.
        """
        return student in self._residents

    @property
    def is_empty(self) -> bool:
        """Проверяет, пустует ли комната."""
        return len(self._residents) == 0

    def evict_all(self) -> None:
        """Массово выселяет всех проживающих (например, на время летнего ремонта)."""
        self._residents.clear()


class Dormitory:
    """
    Здание общежития, состоящее из жилых комнат.

    Attributes:
        number (int): Номер корпуса общежития.
        address (str): Физический адрес здания.
    """

    def __init__(self, number: int, address: str) -> None:
        self.number = number
        self.address = address
        self._rooms: list[Room] = []

    def add_room(self, room: Room) -> None:
        """
        Добавляет новую жилую комнату в план общежития.

        Args:
            room (Room): Экземпляр комнаты.

        Raises:
            ValueError: Если комната с таким номером уже существует.
        """
        if any(r.number == room.number for r in self._rooms):
            raise ValueError(f"Комната {room.number} уже есть в плане общежития.")
        self._rooms.append(room)

    def find_room_for_student(self, student: Student) -> Room | None:
        """
        Ищет комнату, за которой закреплен указанный студент.

        Args:
            student (Student): Искомый студент.

        Returns:
            Room | None: Объект комнаты, если студент найден, иначе None.
        """
        for room in self._rooms:
            if room.has_resident(student):
                return room
        return None

    def get_available_rooms(self) -> list[Room]:
        """
        Фильтрует и возвращает список комнат со свободными местами.

        Returns:
            list[Room]: Список доступных для заселения комнат.
        """
        return [room for room in self._rooms if room.free_beds > 0]

    @property
    def occupancy_rate(self) -> float:
        """
        Агрегация: вычисляет процент заполненности общежития (отношение занятых мест к общему числу).
        """
        if not self._rooms:
            return 0.0

        total_beds = sum(r.capacity for r in self._rooms)
        taken_beds = sum(r.capacity - r.free_beds for r in self._rooms)

        return round((taken_beds / total_beds) * 100, 2)