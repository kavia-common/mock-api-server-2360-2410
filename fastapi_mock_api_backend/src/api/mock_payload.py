"""
Holds the mock JSON payload returned by the API.

IMPORTANT:
- This module is intentionally a simple constant so the `/mock` endpoint can return
  the payload *exactly* as provided by the user (no additional wrapper keys).
- Update `MOCK_PAYLOAD` to match the authoritative payload.
"""

from typing import Any, Dict

# The mock JSON payload returned by GET /mock.
#
# Replace this entire object with the exact user-provided JSON payload.
MOCK_PAYLOAD: Dict[str, Any] = {
    "todo": "AUTHORITATIVE_PAYLOAD_NOT_LOADED",
    "note": (
        "The user-provided payload attachment was not found at runtime. "
        "Update src/api/mock_payload.py:MOCK_PAYLOAD with the exact JSON."
    ),
}
