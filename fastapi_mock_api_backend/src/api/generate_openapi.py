"""
Utility script to generate the OpenAPI schema for this service.

Run (from container root):
  python -m src.api.generate_openapi

It will write the generated schema to:
  fastapi_mock_api_backend/interfaces/openapi.json
"""

import json
import os

from src.api.main import app

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file (relative to container root)
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(openapi_schema, f, indent=2)
    f.write("\n")
