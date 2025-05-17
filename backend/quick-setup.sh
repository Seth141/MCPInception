#!/bin/bash

# Navigate to the backend directory
cd "$(dirname "$0")/.."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  uv venv
  echo "Virtual environment created at .venv"
fi

echo "To run the backend, use:"
echo "cd backend && uv run -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo
echo "Or simply:"
echo "cd backend && uv run main.py"