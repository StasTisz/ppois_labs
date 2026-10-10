from __future__ import annotations

import uuid


class Classroom:
    """
    Учебная аудитория.

    Attributes:
        room_id (str): Уникальный идентификатор аудитории (UUID).
        number (str): Номер аудитории (например, "412-2").
        capacity (int): Максимальная вместимость (количество посадочных мест).
        has_projector (bool): Наличие мультимедийного проектора.
        has_computers (bool): Наличие персональных компьютеров для студентов.
        is_available (bool): Доступна ли аудитория для проведения занятий (не на ремонте).
    """

    def __init__(
            self, number: str, capacity: int, has_projector: bool = False, has_computers: bool = False
    ) -> None:
        self.room_id = str(uuid.uuid4())
        self.number = number
        self.capacity = capacity
        self.has_projector = has_projector
        self.has_computers = has_computers
        self.is_available = True

    def close_for_maintenance(self) -> None:
        """Блокирует аудиторию (закрывает на ремонт)."""
        self.is_available = False

    def open_classroom(self) -> None:
        """Снимает блокировку с аудитории после завершения ремонта."""
        self.is_available = True

    def equip_with_computers(self, update_capacity_by: int = 0) -> None:
        """
        Модернизирует аудиторию в компьютерный класс.

        Args:
            update_capacity_by (int): Изменение количества мест

        Raises:
            ValueError: Если после переоборудования в аудитории не остается мест.
        """
        new_capacity = self.capacity + update_capacity_by
        if new_capacity <= 0:
            raise ValueError(
                f"Недопустимая вместимость: {new_capacity}. "
                f"Аудитория должна вмещать хотя бы одного человека."
            )

        self.has_computers = True
        self.capacity = new_capacity

    def remove_projector(self) -> None:
        """Списывает нерабочий проектор из аудитории."""
        self.has_projector = False
