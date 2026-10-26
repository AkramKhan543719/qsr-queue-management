
from dataclasses import dataclass
from typing import Protocol


@dataclass
class AnalyticsResult:
    camera_id: int
    customer_count: int
    queue_length: int
    estimated_wait_seconds: int
    fps: float
    timestamp: str
    evidence_path: str | None = None


class AnalyticsProvider(Protocol):
    def get_latest(self, camera_id: int) -> AnalyticsResult:
        ...
