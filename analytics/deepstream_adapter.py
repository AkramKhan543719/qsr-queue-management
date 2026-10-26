
from analytics.base import AnalyticsResult


class DeepStreamAnalytics:
    """
    Integration boundary for NVIDIA DeepStream.

    Replace the placeholder with actual DeepStream metadata or
    an edge-agent API connection when the GPU pipeline is ready.
    """

    def get_latest(self, camera_id: int) -> AnalyticsResult:
        raise NotImplementedError(
            "DeepStream pipeline is not connected yet. "
            "Configure the edge agent before selecting this provider."
        )
