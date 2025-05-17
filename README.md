# MCPInception

## Project Structure

This project is organized with a dedicated `backend` directory that manages its own Python environment and dependencies.

-   **Backend Logic**: All backend Python code and the setup script (`create-venv.sh`) reside in the `backend/` directory.
-   **Package Management**: The backend uses [uv](https://github.com/astral-sh/uv) with `backend/pyproject.toml` for dependency management.
-   **Virtual Environment**: The Python virtual environment (`.venv`) is located at `backend/.venv/`.

## Backend Setup & Execution

### Python Version
The backend is built using Python 3.12.

### Environment Setup
1.  **Prerequisites**:
    *   Ensure you have `uv` installed.
    *   Ensure you have PostgreSQL installed.

2.  **PostgreSQL Database Setup**:
    The backend requires a PostgreSQL database named `mcp`.
    *   **Ensure PostgreSQL Server is Running**:
        On macOS (if installed via Homebrew), you can usually start it using:
        ```bash
        brew services start postgresql
        # (The service name might be version-specific, e.g., postgresql@14)
        ```
        Verify it's running using `pg_isready -h localhost -p 5432` or check `brew services list`.
    *   **Create the `mcp` Database**:
        Connect to PostgreSQL using `psql`. You'll typically connect to the default `postgres` database as your macOS user (e.g., `sudo` if your username is `sudo`):
        ```bash
        psql -U your_macos_username -d postgres
        # Example: psql -U sudo -d postgres
        ```
        Once in the `psql` prompt (e.g., `postgres=#`), execute:
        ```sql
        CREATE DATABASE mcp;
        ```
        If it already exists, you'll see an error message, which is fine. Type `\q` to exit `psql`.

3.  **Navigate to Backend and Run Python Environment Setup Script**:
    First, change into the `backend` directory from the project root:
    ```bash
    cd backend
    ```
    Then, execute the setup script:
    ```bash
    ./create-venv.sh
    ```
    This script, now located in and run from `backend/`, will:
    *   Create a Python virtual environment at `backend/.venv/` (i.e., `./.venv/` relative to the script).
    *   Install all necessary Python dependencies (like `psycopg2`, `beautifulsoup4`, `requests`, etc.) as listed in `backend/pyproject.toml`.
    *   Set up `./.env.example` and `./.env` within the `backend` directory.

4.  **Manual Virtual Environment Activation** (Optional):
    If you need to manually activate the backend's virtual environment:
    From the `backend/` directory:
    ```bash
    source .venv/bin/activate  # On macOS/Linux
    # or .venv\Scripts\activate on Windows
    ```
    Alternatively, from the project root:
    ```bash
    source backend/.venv/bin/activate # On macOS/Linux
    ```

### Environment Variables
The backend uses a `./.env` file (within the `backend` directory) to manage environment-specific variables, particularly database credentials if they differ from defaults.

1.  The setup script (`./create-venv.sh`, run from `backend/`) will attempt to copy `./.env.example` to `./.env` if the latter does not exist.
2.  After running the setup script, open `backend/.env` (i.e., `./.env` if you are in the `backend` directory) and update placeholder values with your actual configuration details if needed (e.g., API keys, non-default database URLs/credentials).

**Important:** The `backend/.env` file should *not* be committed to version control. Ensure `backend/.env` is listed in your `.gitignore` file.

### Running Python Scripts

The primary example script is `template.py`, which demonstrates web scraping using `BeautifulSoup` and database interaction with `psycopg2`.

**Dependencies**: The `./create-venv.sh` script installs all necessary Python packages (including `psycopg2` for PostgreSQL, `beautifulsoup4` and `requests` for web scraping, `python-dotenv` for environment variables, and `pydantic` for data validation) from `backend/pyproject.toml` into the virtual environment.

**Execution**: To execute Python scripts located within the `backend` directory, it's recommended to run `uv` from within that directory. `uv run` will automatically use the `backend/.venv`.

1.  Ensure you are in the `backend` directory:
    ```bash
    # If not already there from a previous step:
    # cd backend 
    ```
2.  Run the `template.py` script, providing a full valid URL as an argument:
    ```bash
    uv run template.py <your_target_url>
    # Example:
    # uv run template.py http://example.com
    ```
    The script will attempt to connect to the `mcp` PostgreSQL database (using credentials typically defined in `template.py` or via environment variables) and then fetch and parse the content from the provided URL.