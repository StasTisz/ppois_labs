from __future__ import annotations

import uuid
from datetime import datetime


class FlightPlan:
    def __init__(self, origin: str, destination: str, scheduled_time: datetime) -> None:
        self.plan_id = str(uuid.uuid4())
        self.origin = origin
        self.destination = destination
        self.scheduled_time = scheduled_time
        self.air_corridor = f"{origin}-{destination}-CORRIDOR-1"
