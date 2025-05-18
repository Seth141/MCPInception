#!/bin/bash

# Script is intended to be run from the 'backend' directory.
# Project root is one level up from this script's assumed location.
PROJECT_ROOT_REL=".." # Relative path to project root from backend/
BACKEND_DIR_REL="."     # This script runs within the backend directory (current dir)

# Get absolute paths for robust messaging
SCRIPT_LOCATION_ABS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd) # Should be .../backend
PROJECT_ROOT_ABS=$(cd "$SCRIPT_LOCATION_ABS/$PROJECT_ROOT_REL" && pwd) # Should be .../MCPInception
BACKEND_DIR_ABS="$SCRIPT_LOCATION_ABS" # Current directory, i.e., .../backend

VENV_NAME=".venv" # Name of the virtual environment directory
VENV_PATH_REL="./$VENV_NAME" # Relative path to venv from script location (backend/)
# Absolute path helpers
VENV_PATH_ABS="$BACKEND_DIR_ABS/$VENV_NAME"
UV_LOCK_PATH="$BACKEND_DIR_ABS/uv.lock"

echo "Project Root (determined from script location): $PROJECT_ROOT_ABS"
echo "Backend Directory (current): $BACKEND_DIR_ABS"
echo "Working directory: $BACKEND_DIR_ABS"
echo "Setting up Python 3.12 virtual environment in '$VENV_PATH_ABS' using uv..."

# Remove existing uv.lock to ensure fresh dependency resolution
echo "Checking for existing $UV_LOCK_PATH file..."
if [ -f "$UV_LOCK_PATH" ]; then
    echo "Found $UV_LOCK_PATH. Removing it to ensure fresh dependency resolution..."
    rm "$UV_LOCK_PATH"
    echo "$UV_LOCK_PATH removed."
else
    echo "$UV_LOCK_PATH not found, proceeding with setup."
fi
echo # Add a blank line for readability

# We are already in the backend directory, so uv commands run here.
# Create the virtual environment in ./venv (relative to backend/)
if uv venv "$VENV_NAME"; then # Explicitly name the venv dir
    echo "Virtual environment '$VENV_PATH_ABS' created successfully in $BACKEND_DIR_ABS."
else
    echo "Failed to create virtual environment in $BACKEND_DIR_ABS."
    exit 1
fi

# Activate the virtual environment and install dependencies
echo "Installing dependencies from ./pyproject.toml and the project in editable mode..."
(
  source "$VENV_PATH_REL/bin/activate"
  # pyproject.toml is in the current directory (.)
  # '.' refers to the current directory (backend) as the project to install
  if uv pip sync pyproject.toml && uv pip install -e .; then
      echo "Dependencies installed successfully into '$VENV_PATH_ABS'."
  else
      echo "Failed to install dependencies into '$VENV_PATH_ABS'."
      exit 1
  fi
)
INSTALL_STATUS=$?
if [ $INSTALL_STATUS -ne 0 ]; then
    echo "Dependency installation failed. Exiting script."
    exit $INSTALL_STATUS
fi

echo "Setting up backend environment configuration file..."
ENV_EXAMPLE_PATH_REL="./.env.example"
ENV_PATH_REL="./.env"
ENV_EXAMPLE_PATH_ABS="$BACKEND_DIR_ABS/.env.example"
ENV_PATH_ABS="$BACKEND_DIR_ABS/.env"

# Ensure a .env.example exists in the current (backend) folder
if [ ! -f "$ENV_EXAMPLE_PATH_ABS" ]; then
    echo "Creating a template $ENV_EXAMPLE_PATH_ABS..."
    echo "# Example environment variables for the backend" > "$ENV_EXAMPLE_PATH_ABS"
    echo "DATABASE_URL=\"your_database_url_here\"" >> "$ENV_EXAMPLE_PATH_ABS"
    echo "API_KEY=\"your_api_key_here\"" >> "$ENV_EXAMPLE_PATH_ABS"
    echo "SECRET_KEY=\"a_very_secret_key\"" >> "$ENV_EXAMPLE_PATH_ABS"
    echo "Example content written to $ENV_EXAMPLE_PATH_ABS."
fi

# Copy .env.example to .env in the current (backend) folder if .env doesn't exist
if [ ! -f "$ENV_PATH_ABS" ]; then
    echo "Copying $ENV_EXAMPLE_PATH_ABS to $ENV_PATH_ABS..."
    if cp "$ENV_EXAMPLE_PATH_ABS" "$ENV_PATH_ABS"; then
        echo "$ENV_PATH_ABS created. IMPORTANT: Please open this file and update it with your actual configuration values."
    else
        echo "Warning: Failed to copy $ENV_EXAMPLE_PATH_ABS to $ENV_PATH_ABS. Please do this manually."
    fi
else
    echo "$ENV_PATH_ABS already exists. Please ensure it is up to date with necessary variables from $ENV_EXAMPLE_PATH_ABS."
fi

echo
echo "---------------------------------------------------------------------"
echo "Setup complete for the backend environment!"
echo "---------------------------------------------------------------------"
echo "- Virtual environment '$VENV_NAME' is ready at $BACKEND_DIR_ABS/$VENV_NAME"
echo "- Dependencies are installed into this virtual environment."
echo "- Backend environment file is at $BACKEND_DIR_ABS/.env."
echo "  (It was created from $ENV_EXAMPLE_PATH_ABS if it was missing)."
echo "  ACTION REQUIRED: If $ENV_PATH_ABS was just created, please edit it now with your specific settings."
echo
echo "To activate this virtual environment manually (from '$BACKEND_DIR_ABS' directory):"
echo "  source $VENV_PATH_REL/bin/activate"
echo
echo "To run scripts using this environment (from '$BACKEND_DIR_ABS' directory):"
echo "  uv run your_script_name.py"
echo "---------------------------------------------------------------------"
echo

exit 0
