import os
from typing import Any, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
#
# NOTE: If you need to allow a different origin in your environment, request setting:
#   CORS_ALLOW_ORIGINS="http://localhost:XXXX,http://127.0.0.1:YYYY"
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
        "- `GET /health` returns service status.\n\n"
        "NOTE: `/mock` returns the payload *as-is* (not wrapped) to match frontend expectations."
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


# PUBLIC_INTERFACE
@app.get(
    "/health",
    tags=["Health"],
    operation_id="get_health",
    summary="Health check",
    description="Returns the health status of the service.",
)
def health() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: `{"status": "ok"}` when the service is up.
    """
    return {"status": "ok"}


# Import the payload from a dedicated module so it can be updated independently.
from src.api.mock_payload import MOCK_PAYLOAD  # noqa: E402  (import after app setup is ok here)


# PUBLIC_INTERFACE
@app.get(
    "/mock",
    tags=["Mock"],
    operation_id="get_mock_payload",
    summary="Get mock JSON payload",
    description=(
        "Returns the mock JSON payload intended for frontend development/testing.\n\n"
        "The response body is the payload itself (no extra wrapper fields)."
    ),
    response_model=dict[str, Any],
)
def get_mock() -> dict[str, Any]:
    """
    Mock payload endpoint.

    Returns:
        dict[str, Any]: The mock JSON payload as the *top-level* response object.

    Notes:
        The payload includes top-level metadata fields:
        - request_id
        - version
        - generated_at
    """
    # Return exactly the payload (no wrapper like {"payload": ...}).
    return MOCK_PAYLOAD
