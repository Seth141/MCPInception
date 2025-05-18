# YC Companies MCP Server

This project exposes YC company batch data via Model Context Protocol (MCP).

## Features

- Lists companies from Y Combinator batches via MCP resources
- Accessible through Claude Desktop or any MCP client
- Resource pattern: `mcp://yc/{batch}.json`

## Setup

1. From the `backend` directory, run the setup script:
   ```bash
   ./create-venv.sh
   ```

2. This creates a Python virtual environment and installs all dependencies.

## Using the MCP Server

### Simple Testing Approach

See the `HOW_TO_MCP` file for the most reliable way to test the server:

```bash
# Terminal 1 - Run the MCP server
cd backend
uv run yc_mcp_server.py

# Terminal 2 - Test by directly accessing the YC API endpoint
curl -s "https://yc-oss.github.io/api/batches/summer-2015.json"
```

This confirms that the YC API is accessible and the data format is valid.

### Integration with Claude Desktop

1. Edit your Claude Desktop configuration at:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. Add the following to configure the MCP server (replace `$REPO_PATH` with your actual path):

   ```json
   {
     "mcpServers": {
       "yc": {
         "command": "uv",
         "args": [
           "--directory",
           "$REPO_PATH/backend",
           "run",
           "yc_mcp_server.py"
         ]
       }
     }
   }
   ```

   For flexible configuration, you can use environment variables in Windows/bash:

   **Windows PowerShell**:
   ```powershell
   $REPO_PATH = (Get-Location).Path
   Set-Content -Path "$HOME\AppData\Roaming\Claude\claude_desktop_config.json" -Value @"
   {
     "mcpServers": {
       "yc": {
         "command": "uv",
         "args": [
           "--directory",
           "$REPO_PATH\backend",
           "run",
           "yc_mcp_server.py"
         ]
       }
     }
   }
   "@
   ```

   **macOS/Linux Bash**:
   ```bash
   REPO_PATH="$(pwd)"
   mkdir -p ~/Library/Application\ Support/Claude/
   cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << EOL
   {
     "mcpServers": {
       "yc": {
         "command": "uv",
         "args": [
           "--directory",
           "$REPO_PATH/backend",
           "run",
           "yc_mcp_server.py"
         ]
       }
     }
   }
   EOL
   ```

3. Restart Claude Desktop application

4. Click on the hammer icon in Claude Desktop to access tools

5. Ask questions like:
   - "Show me YC companies from Summer 2015"
   - "What companies were in the Winter 2012 batch?"

