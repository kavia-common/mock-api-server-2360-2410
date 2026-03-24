import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


def _parse_cors_origins(raw: Optional[str]) -> List[str]:
    """
    Parse a comma-separated list of origins from an env var.

    Examples:
      "http://localhost:3000,http://127.0.0.1:5173"
    """
    if not raw:
        return []
    return [o.strip() for o in raw.split(",") if o.strip()]


# Configure CORS:
# - Default for local development (common dev ports).
# - Can be overridden with CORS_ALLOW_ORIGINS env var (comma-separated).
_default_dev_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
_allow_origins = _parse_cors_origins(os.getenv("CORS_ALLOW_ORIGINS")) or _default_dev_origins

openapi_tags = [
    {"name": "Health", "description": "Service health and readiness endpoints."},
    {"name": "Mock", "description": "Endpoints serving mock payloads for frontend consumption."},
]

app = FastAPI(
    title="FastAPI Mock API Backend",
    description=(
        "A backend-only mock API built with FastAPI.\n\n"
        "- `GET /mock` returns a fixed JSON payload for frontend consumption.\n"
        "- `GET /health` returns service status.\n"
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str = Field(..., description="Service health status. 'ok' when healthy.")


class MockPayloadResponse(BaseModel):
    """Response model for the /mock endpoint."""

    payload: Dict[str, Any] = Field(..., description="Mock JSON payload.")


# PUBLIC_INTERFACE
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    operation_id="get_health",
    summary="Health check",
    description="Returns the health status of the service.",
)
def health() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: `{"status": "ok"}` when the service is up.
    """
    return HealthResponse(status="ok")


# The "provided JSON payload" is intended to be implemented as a fixed mock object.
# TODO: Replace MOCK_PAYLOAD with the exact JSON from the user_input_ref attachment.
# NOTE: In this execution environment, the referenced attachment path was not found, so the
# exact payload could not be loaded automatically.
MOCK_PAYLOAD: Dict[str, Any] = {
    "error": "Attachment not available in runtime environment",
    "detail": (
        "The user-provided JSON payload must be pasted here verbatim (as a Python dict) "
        "once the attachment is accessible."
    ),
}


# PUBLIC_INTERFACE
@app.get(
    "/mock",
    response_model=MockPayloadResponse,
    tags=["Mock"],
    operation_id="get_mock_payload",
    summary="Get mock JSON payload",
    description="Returns a fixed JSON payload intended for frontend development/testing.",
)
def get_mock() -> MockPayloadResponse:
    """
    Mock payload endpoint.

    Returns:
        MockPayloadResponse: An object with a `payload` field containing the mock JSON.
    """
    return MockPayloadResponse(payload=MOCK_PAYLOAD)
