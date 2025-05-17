#!/bin/bash

### At ROOT level run
### ./setup/create-venv.sh
PWD="$(realpath "$0")"
printf "PWD: %s\n" "$PWD"

# one level up from current
ROOT="$(realpath "$(dirname "$0")/..")"
printf "ROOT: %s\n" "$ROOT"

cd "$ROOT"
if [ -d "$ROOT/.venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf "$ROOT/.venv"
fi

echo "Creating new virtual environment..."
uv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    cd "$PWD"
    exit 1
fi

echo "Installing dependencies..."
# Install project and all dependencies from pyproject.toml
. .venv/bin/activate && uv pip install -e .
if [ $? -ne 0 ]; then
    echo "Failed to install main dependencies."
    cd "$PWD"
    exit 1
fi

# Install development dependencies
echo "Installing development dependencies..."
. .venv/bin/activate && uv pip install -e ".[dev]"
if [ $? -ne 0 ]; then
    echo "Warning: Failed to install development dependencies, but main dependencies are installed."
fi

# echo "Deactivating virtual environment..."
# deactivate
cd "$PWD"
echo "Created venv, activated, installed dependencies."
echo "Exiting successfully."
echo "To activate the virtual environment, run:"
echo
echo ". .venv/bin/activate"
echo
echo "uv run <script_name>.py activates the venv so manual run not needed"
echo
