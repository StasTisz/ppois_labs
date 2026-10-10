from __future__ import annotations

from lab2.domain.people.employee import Employee


class Dean(Employee):
    """
    Декан факультета. Подписывает приказы и руководит факультетом.
    """
    DEFAULT_DEGREE = "К.т.н."
    DEFAULT_POSITION = "Декан"

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", degree: str = DEFAULT_DEGREE) -> None:
        super().__init__(first_name, last_name, middle_name, position=self.DEFAULT_POSITION)
        self.degree = degree

    def sign_order(self, order_text: str) -> str:
        """
        Подписывает приказ по факультету.

        Args:
            order_text (str): Текст приказа.

        Returns:
            str: Форматированная строка подписанного приказа.
        """
        return f"ПРИКАЗ УТВЕРЖДЕН: {order_text} | Подписант: декан {self.full_name}"
