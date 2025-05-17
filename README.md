# MCPInception

## Project Setup & Execution

This project uses [uv](https://github.com/astral-sh/uv) for Python package management and task running. All dependencies are managed via the `pyproject.toml` file.

### Python Version
The project is built using Python 3.12.

### Environment Setup
1.  Ensure you have `uv` installed (if not already managed by the setup script).
2.  Run the setup script to create the virtual environment and install dependencies:
    ```bash
    ./setup/create-venv.sh
    ```
    This script will create a `.venv` directory in the project root and install all dependencies listed in `pyproject.toml`.
3.  If you need to activate the environment manually (e.g., for direct terminal use outside of `uv run`), you can do so after the setup script has run:
    ```bash
    source .venv/bin/activate  # On macOS/Linux
    # or .venv\Scripts\activate on Windows
    ```

### Environment Variables
This project uses a `.env` file to manage environment-specific variables. A template is provided as `.env.example`.

1.  Copy the example file to a new `.env` file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and update the placeholder values with your actual configuration details (e.g., API keys, database URLs).

**Important:** The `.env` file should *not* be committed to version control. Ensure it is listed in your `.gitignore` file.

### Running Python Scripts
To execute Python scripts, use `uv run`. This command automatically uses the project's virtual environment (created by `./setup/create-venv.sh`) and ensures the script runs with the correct Python interpreter (3.12) and all specified dependencies. You do not need to manually activate the virtual environment before using `uv run`.

Example:
```bash
uv run your_script_name.py
```