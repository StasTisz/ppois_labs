from __future__ import annotations

import uuid

from lab3.domain.exceptions import SecurityCheckFailedException
from lab3.domain.security.customs_declaration import CustomsDeclaration


class CustomsControl:
    MAX_CASH_ALLOWED_USD = 10000.0

    def __init__(self) -> None:
        self.control_id = str(uuid.uuid4())

    def inspect_declaration(self, declaration: CustomsDeclaration) -> None:
        if declaration.cash_amount > self.MAX_CASH_ALLOWED_USD:
            raise SecurityCheckFailedException(
                f"Сумма {declaration.cash_amount}$ превышает лимит вывоза "
                f"без дополнительных разрешений ({self.MAX_CASH_ALLOWED_USD}$)."
            )
        declaration.approve()
