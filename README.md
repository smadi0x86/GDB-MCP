[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/smadi0x86-mdb-mcp-badge.png)](https://mseep.ai/app/smadi0x86-mdb-mcp)

# Multi-Debugger MCP Server (LLDB and GDB)

A Model Context Protocol server that provides debugging functionality for both GDB and LLDB debuggers, for use with Claude Desktop, VSCode Copilot, or other AI assistants.

<p align="center">
  <img src="images/gdb-mcp.png" alt="GDB MCP Server" width="600">
</p>

## Quick Start

```bash
uv sync
uv venv
uv run server.py
```

## Integration

Note that you can use `uv run` to run the server.py script or you can use `uv venv` to create a virtual environment and then run `/home/youruser/dev/personal/GDB-MCP/.venv/bin/python /home/youruser/dev/personal/GDB-MCP/server.py`.

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gdb": {
      "command": "uv",
      "args": ["run", "/home/youruser/dev/personal/GDB-MCP/server.py"],
      "disabled": false
    }
  }
}
```

### VSCode Copilot

If you're using WSL:

```json
 "mcp": {
    "servers": {
      "my-mcp-server-4dc36648": {
        "type": "stdio",
        "command": "wsl",
        "args": [
          "/home/youruser/dev/personal/GDB-MCP/.venv/bin/python",
          "/home/youruser/dev/personal/GDB-MCP/server.py"
        ]
      }
    }
  }
```

If you're not using WSL:

```json
  "mcp": {
    "servers": {
      "my-mcp-server-db89eee1": {
        "type": "stdio",
        "command": "/home/youruser/dev/personal/GDB-MCP/.venv/bin/python",
        "args": ["/home/youruser/dev/personal/GDB-MCP/server.py"]
      }
    }
  }
```

### Windsurf

```json
{
  "mcpServers": {
    "debugger-mcp": {
      "command": "python3",
      "args": ["/Users/youruser/dev/GDB-MCP/server.py"]
    }
  }
}
```

## Experimental LLDB Support (macOS)

This project includes experimental native LLDB support alongside GDB, with automatic debugger selection.

<p align="center">
  <img src="images/multi-debugger.png" alt="Multi-Debugger MCP Server" width="600">
</p>

### Installation

To enable LLDB support on macOS, install LLVM (which includes LLDB) and python via Homebrew:

```bash
# Install LLDB for supporting python3.14 bindings
brew install llvm python3

# Install MCP and debugging dependencies
pip3 install mcp pygdbmi --break-system-packages
```

## Available Tools

### Unified Tools

- `debugger_status()`: Show available debuggers and their status
- `debugger_start()`: Start debugging session with auto-detected debugger
- `debugger_terminate(session_id)`: Terminate debugging session
- `debugger_list_sessions()`: List all active debugging sessions
- `debugger_command(session_id, command)`: Execute debugger command

### LLDB Tools

- `lldb_start()`: Start new LLDB debugging session
- `lldb_terminate(session_id)`: Terminate LLDB debugging session
- `lldb_list_sessions()`: List all active LLDB sessions
- `lldb_command(session_id, command)`: Execute arbitrary LLDB command

### GDB Tools

- `gdb_start(gdb_path)`: Start new GDB debugging session
- `gdb_terminate(session_id)`: Terminate GDB debugging session
- `gdb_list_sessions()`: List all active GDB sessions
- `gdb_command(session_id, command)`: Execute any GDB command

> Use `*_command()` functions for all advanced debugger operations, your LLM client should already know how to use it, but it doesn't hurt to mention it.

### Checking Status

You can verify debugger availability:

```python
from modules.lldb import LLDBSessionManager
from modules.gdb import GDBSessionManager

print("LLDB available:", LLDBSessionManager.is_available())
print("GDB available:", GDBSessionManager.is_available())
```

## Testing

```bash
uv run python run-tests.py --check-deps
uv run python run-tests.py --type all
```

## Examples

Check the `examples` directory for example prompts.

> Example binaries are compiled to `arm64` and `amd64`, pick the one that matches your system architecture.

## License

This project is licensed under the GNU Version 3.0 License, see the LICENSE file for details.
