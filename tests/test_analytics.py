
from analytics.mock_analytics import MockAnalytics


def test_mock_analytics_returns_queue_metrics():
    provider = MockAnalytics()
    result = provider.get_latest(camera_id=1)

    assert result.camera_id == 1
    assert result.customer_count >= 0
    assert result.queue_length >= 0
    assert result.estimated_wait_seconds >= 0
    assert result.fps >= 0
    assert result.timestamp
