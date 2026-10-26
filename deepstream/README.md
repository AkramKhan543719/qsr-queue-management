
# QSR DeepStream Integration

This folder contains a starter integration client for the QSR backend.

## Current status

- The DeepStream metadata endpoint is not configured yet.
- The expected edge-agent endpoint is a placeholder contract.
- This code does not run NVIDIA DeepStream inference.
- Actual customer counts and queue metrics must come from the configured
  DeepStream pipeline.

## Configuration

Set these environment variables when the edge agent is available:

- `DEEPSTREAM_METADATA_URL`
- `QSR_API_URL`
- `POLL_INTERVAL_SECONDS`

## Run

From the project root:

```powershell
python -m deepstream.edge_agent
```

The edge agent must expose the expected metadata endpoint before this
integration can work.
