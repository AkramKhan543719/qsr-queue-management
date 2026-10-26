
import requests


class DeepStreamMetadataClient:
    """Client for a future DeepStream edge-agent metadata API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get_latest(self, camera_id: int) -> dict:
        """
        Expected edge-agent contract:
        GET /cameras/{camera_id}/metadata/latest

        The actual endpoint must match your edge-agent API.
        """
        response = self.session.get(
            f"{self.base_url}/cameras/{camera_id}/metadata/latest",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
