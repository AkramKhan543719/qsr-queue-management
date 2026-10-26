
import time
import requests

from deepstream.config import (
    DEEPSTREAM_METADATA_URL,
    QSR_API_URL,
    POLL_INTERVAL_SECONDS,
)
from deepstream.metadata_client import DeepStreamMetadataClient


def main():
    username = input("QSR username: ").strip()
    password = input("QSR password: ").strip()

    session = requests.Session()

    login_response = session.post(
        f"{QSR_API_URL}/api/auth/login",
        json={"username": username, "password": password},
        timeout=15,
    )
    login_response.raise_for_status()

    token = login_response.json()["access_token"]
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })

    metadata_client = DeepStreamMetadataClient(
        DEEPSTREAM_METADATA_URL
    )

    cameras_response = session.get(
        f"{QSR_API_URL}/api/cameras",
        timeout=15,
    )
    cameras_response.raise_for_status()
    cameras = cameras_response.json()

    if not cameras:
        print("No registered cameras found.")
        return

    print("DeepStream metadata polling started.")
    print("Stop with Ctrl+C.")

    try:
        while True:
            for camera in cameras:
                if not camera.get("is_active", True):
                    continue

                camera_id = camera["id"]

                try:
                    metadata = metadata_client.get_latest(camera_id)

                    customer_count = int(metadata["customer_count"])
                    queue_length = int(metadata["queue_length"])
                    wait_seconds = int(
                        metadata["estimated_wait_seconds"]
                    )
                    fps = float(metadata.get("fps", 0.0))

                    payload = {
                        "camera_id": camera_id,
                        "customer_count": customer_count,
                        "queue_length": queue_length,
                        "estimated_wait_seconds": wait_seconds,
                        "fps": fps,
                    }

                    response = session.post(
                        f"{QSR_API_URL}/api/queue",
                        json=payload,
                        timeout=15,
                    )
                    response.raise_for_status()

                    print(
                        f"Camera {camera_id}: "
                        f"customers={customer_count}, "
                        f"queue={queue_length}, "
                        f"wait={wait_seconds}s"
                    )

                except (requests.RequestException, KeyError, ValueError) as exc:
                    print(f"Camera {camera_id} failed: {exc}")

            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nEdge agent stopped.")


if __name__ == "__main__":
    main()
