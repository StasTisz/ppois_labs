from __future__ import annotations

import uuid
from datetime import datetime


class Visa:
    def __init__(self, country: str, expiration_date: datetime) -> None:
        self.visa_id = str(uuid.uuid4())
        self.country = country
        self.expiration_date = expiration_date

    def is_valid(self, current_date: datetime) -> bool:
        return current_date <= self.expiration_date
