
import time
from pathlib import Path

import cv2
import requests
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
API_URL = "http://127.0.0.1:8000"

# Change this if your trained person-detection model is available.
MODEL_NAME = "yolo11n.pt"
SAMPLE_EVERY_SECONDS = 2
AVERAGE_WAIT_SECONDS_PER_PERSON = 30

def main():
    print("Loading YOLO model...")
    model = YOLO(MODEL_NAME)

    session = requests.Session()
    session.headers["Content-Type"] = "application/json"

    username = input("QSR username: ").strip()
    password = input("QSR password: ").strip()

    login = session.post(
        f"{API_URL}/api/auth/login",
        json={"username": username, "password": password},
        timeout=30,
    )
    if not login.ok:
        raise RuntimeError(f"Login failed: {login.status_code} {login.text}")

    session.headers["Authorization"] = (
        f"Bearer {login.json()['access_token']}"
    )

    videos = sorted(VIDEO_DIR.glob("*.mp4"))
    if not videos:
        raise FileNotFoundError(f"No MP4 videos found in {VIDEO_DIR}")

    for video in videos:
        print(f"\nRegistering video: {video.name}")
        camera_response = session.post(
            f"{API_URL}/api/cameras",
            json={
                "name": video.stem,
                "location": "Local video",
                "source_type": "video",
                "source_uri": str(video.resolve()),
                "is_active": True,
            },
            timeout=30,
        )

        if camera_response.status_code == 409:
            print("Camera already exists; skipping registration.")
            print("Please use a new camera name or check the existing camera ID.")
            continue

        if not camera_response.ok:
            print("Camera registration failed:", camera_response.status_code,
                  camera_response.text)
            continue

        camera_id = camera_response.json()["id"]
        cap = cv2.VideoCapture(str(video))
        if not cap.isOpened():
            print("Cannot open video:", video)
            continue

        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        frame_step = max(1, int(fps * SAMPLE_EVERY_SECONDS))
        frame_index = 0
        records_sent = 0

        print(f"Processing {video.name} (camera ID {camera_id})")

        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                if frame_index % frame_step == 0:
                    results = model.predict(
                        frame,
                        classes=[0],
                        conf=0.35,
                        verbose=False,
                    )
                    customer_count = len(results[0].boxes)
                    queue_length = customer_count
                    estimated_wait_seconds = (
                        queue_length * AVERAGE_WAIT_SECONDS_PER_PERSON
                    )

                    payload = {
                        "camera_id": camera_id,
                        "customer_count": customer_count,
                        "queue_length": queue_length,
                        "estimated_wait_seconds": estimated_wait_seconds,
                        "fps": round(float(fps), 2),
                    }

                    response = session.post(
                        f"{API_URL}/api/queue",
                        json=payload,
                        timeout=30,
                    )

                    if response.ok:
                        records_sent += 1
                        print(
                            f"{video.name}: people={customer_count}, "
                            f"queue={queue_length}, "
                            f"wait~{estimated_wait_seconds}s"
                        )
                    else:
                        print("Queue API error:", response.status_code,
                              response.text)

                frame_index += 1
        finally:
            cap.release()

        print(f"Finished {video.name}; records sent: {records_sent}")

    print("\nAll videos processed.")

if __name__ == "__main__":
    main()
