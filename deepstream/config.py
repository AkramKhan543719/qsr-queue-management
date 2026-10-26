
import os

# DeepStream edge-agent metadata endpoint.
DEEPSTREAM_METADATA_URL = os.getenv(
    "DEEPSTREAM_METADATA_URL",
    "http://127.0.0.1:9000",
)

# QSR FastAPI backend.
QSR_API_URL = os.getenv(
    "QSR_API_URL",
    "http://127.0.0.1:8000",
)

# Sample interval for metadata polling.
POLL_INTERVAL_SECONDS = float(
    os.getenv("POLL_INTERVAL_SECONDS", "2")
)
