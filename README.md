# MCPInception

## Project Setup & Execution

This project uses [uv](https://github.com/astral-sh/uv) for Python package management and task running. All dependencies are managed via the `pyproject.toml` file.

### Python Version
The project is built using Python 3.12.

### Environment Setup
1.  Ensure you have `uv` installed.
2.  Create a virtual environment in the project root:
    ```bash
    uv venv
    ```
3.  Activate the virtual environment:
    ```bash
    source .venv/bin/activate  # On macOS/Linux
    # or .venv\Scripts\activate on Windows
    ```
4.  Install dependencies from `pyproject.toml`:
    ```bash
    uv pip sync pyproject.toml
    ```

### Running Python Scripts
To execute Python scripts within the project's managed environment, use `uv run`:
```bash
uv run your_script_name.py
```
This ensures the script runs with the correct Python interpreter (3.12) and all specified dependencies.