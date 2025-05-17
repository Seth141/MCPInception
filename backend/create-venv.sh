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

echo "Project Root (determined from script location): $PROJECT_ROOT_ABS"
echo "Backend Directory (current): $BACKEND_DIR_ABS"
echo "Setting up Python 3.12 virtual environment in '$VENV_PATH_REL' using uv..."

# Remove existing uv.lock to ensure fresh dependency resolution
echo "Checking for existing ./uv.lock file..."
if [ -f "./uv.lock" ]; then
    echo "Found ./uv.lock. Removing it to ensure fresh dependency resolution..."
    rm "./uv.lock"
    echo "./uv.lock removed."
else
    echo "./uv.lock not found, proceeding with setup."
fi
echo # Add a blank line for readability

# We are already in the backend directory, so uv commands run here.
# Create the virtual environment in ./venv (relative to backend/)
if uv venv "$VENV_NAME"; then # Explicitly name the venv dir
    echo "Virtual environment '$VENV_PATH_REL' created successfully in $BACKEND_DIR_ABS."
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
      echo "Dependencies installed successfully into '$VENV_PATH_REL'."
  else
      echo "Failed to install dependencies into '$VENV_PATH_REL'."
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

# Ensure a .env.example exists in the current (backend) folder
if [ ! -f "$ENV_EXAMPLE_PATH_REL" ]; then
    echo "Creating a template $ENV_EXAMPLE_PATH_REL..."
    echo "# Example environment variables for the backend" > "$ENV_EXAMPLE_PATH_REL"
    echo "DATABASE_URL=\"your_database_url_here\"" >> "$ENV_EXAMPLE_PATH_REL"
    echo "API_KEY=\"your_api_key_here\"" >> "$ENV_EXAMPLE_PATH_REL"
    echo "SECRET_KEY=\"a_very_secret_key\"" >> "$ENV_EXAMPLE_PATH_REL"
    echo "Example content written to $ENV_EXAMPLE_PATH_REL."
fi

# Copy .env.example to .env in the current (backend) folder if .env doesn't exist
if [ ! -f "$ENV_PATH_REL" ]; then
    echo "Copying $ENV_EXAMPLE_PATH_REL to $ENV_PATH_REL..."
    if cp "$ENV_EXAMPLE_PATH_REL" "$ENV_PATH_REL"; then
        echo "$ENV_PATH_REL created. IMPORTANT: Please open this file and update it with your actual configuration values."
    else
        echo "Warning: Failed to copy $ENV_EXAMPLE_PATH_REL to $ENV_PATH_REL. Please do this manually."
    fi
else
    echo "$ENV_PATH_REL already exists. Please ensure it is up to date with necessary variables from $ENV_EXAMPLE_PATH_REL."
fi

echo
echo "---------------------------------------------------------------------"
echo "Setup complete for the backend environment!"
echo "---------------------------------------------------------------------"
echo "- Virtual environment '$VENV_NAME' is ready at $BACKEND_DIR_ABS/$VENV_NAME"
echo "- Dependencies are installed into this virtual environment."
echo "- Backend environment file is at $BACKEND_DIR_ABS/.env."
echo "  (It was created from $ENV_EXAMPLE_PATH_REL if it was missing)."
echo "  ACTION REQUIRED: If $ENV_PATH_REL was just created, please edit it now with your specific settings."
echo
echo "To activate this virtual environment manually (from '$BACKEND_DIR_ABS' directory):"
echo "  source $VENV_PATH_REL/bin/activate"
echo
echo "To run scripts using this environment (from '$BACKEND_DIR_ABS' directory):"
echo "  uv run your_script_name.py"
echo "---------------------------------------------------------------------"
echo

exit 0
