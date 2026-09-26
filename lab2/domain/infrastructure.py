
from lab2.domain.people import Student


class Room:
    """Жилая комната в общежитии."""

    def __init__(self, number: str, capacity: int = 4):
        self.number = number
        self.capacity = capacity
        self._residents: list[Student] = []

    @property
    def free_beds(self) -> int:
        return self.capacity - len(self._residents)

    def check_in(self, student: Student):
        """Поведение: заселение студента с проверкой лимита мест."""
        if self.free_beds <= 0:
            raise ValueError(f"Блок {self.number} полностью укомплектован.")
        if student in self._residents:
            raise ValueError(f"Студент {student.full_name} уже прописан в этой комнате.")
        self._residents.append(student)

    def evict(self, student: Student):
        """Поведение: выселение."""
        if student not in self._residents:
            raise ValueError("Студент здесь не проживает.")
        self._residents.remove(student)

    @property
    def is_empty(self) -> bool:
        """Проверка, пустует ли комната."""
        return len(self._residents) == 0

    def evict_all(self):
        """Массовое выселение (например, на время летнего ремонта)."""
        self._residents.clear()


class Dormitory:
    """Здание общежития."""

    def __init__(self, number: int, address: str):
        self.number = number
        self.address = address
        self._rooms: list[Room] = []

    def add_room(self, room: Room):
        if any(r.number == room.number for r in self._rooms):
            raise ValueError(f"Комната {room.number} уже есть в плане общежития.")
        self._rooms.append(room)

    def find_room_for_student(self, student: Student) -> Room | None:
        """Поиск комнаты, за которой закреплен конкретный студент."""
        for room in self._rooms:
            if student in room._residents:
                return room
        return None

    def get_available_rooms(self) -> list[Room]:
        """Возвращает список комнат, где есть хотя бы одно свободное место."""
        return [room for room in self._rooms if room.free_beds > 0]

    @property
    def occupancy_rate(self) -> float:
        """Процент заполненности общежития."""
        if not self._rooms:
            return 0.0
        total_beds = sum(r.capacity for r in self._rooms)
        taken_beds = sum(len(r._residents) for r in self._rooms)
        return round((taken_beds / total_beds) * 100, 2)