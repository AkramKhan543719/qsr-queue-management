
from datetime import datetime, timezone

from analytics.base import AnalyticsResult


class MockAnalytics:
    """Demo provider for development before GPU integration."""

    def get_latest(self, camera_id: int) -> AnalyticsResult:
        return AnalyticsResult(
            camera_id=camera_id,
            customer_count=12,
            queue_length=5,
            estimated_wait_seconds=180,
            fps=0.0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            evidence_path=None,
        )
