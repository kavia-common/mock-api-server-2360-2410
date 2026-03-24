#!/bin/bash
cd /home/kavia/workspace/code-generation/mock-api-server-2360-2410/fastapi_mock_api_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

