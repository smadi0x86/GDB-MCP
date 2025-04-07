# GDB MCP Server

An MCP server written in MCP python SDK that enables LLMs to interact with GDB for program debugging and analysis. This tool allows LLMs to perform complex debugging tasks through a generative AI interface.

## Features

- **Session Management**
  - Start and manage multiple GDB sessions
  - Load programs and core dumps
  - Attach to running processes

- **Debugging Commands**
  - Set breakpoints with conditions
  - Step through code (step, next, finish)
  - Continue execution
  - Get backtraces
  - Print variable values
  - Disassemble code
  - List available functions
  - Inspect registers

- **Advanced Features**
  - Multi-session support
  - Working directory configuration
  - Program argument handling
  - Core dump analysis
  - Symbol inspection

> **Note**: The `info functions` and `disassemble` commands are temporarily disabled due to GDB Machine Interface (MI) output parsing issues. These features will be restored in a future update once the output parsing is properly implemented.

## Project Status

- For known issues and current bugs, see [BUGS.md](BUGS.md)
- For planned improvements and features, see [TODO.md](TODO.md)

## Tools Available

```js
GDB_COMMANDS = [
    gdb_start,
    gdb_load,
    gdb_run,
    gdb_command,
    gdb_attach,
    gdb_load_core,
    gdb_set_breakpoint,
    gdb_continue,
    gdb_step,
    gdb_next,
    gdb_finish,
    gdb_backtrace,
    gdb_print,
    gdb_disassemble,
    gdb_info_registers,
    gdb_info_functions,
    gdb_list_sessions,
    gdb_terminate,
]
```
## Installation

1. Clone the repository:
```bash
git clone https://github.com/smadi0x86/gdb-mcp.git
cd gdb-mcp
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Install the package in development mode:
```bash
poetry install
```

## Usage

1. Start the GDB MCP server:
```bash
python3 gdb-mcp.py
```

2. The server will run on stdio, ready to accept commands.

## LLM Client Configuration

### For Claude Desktop

Add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
     "gdb": {
    "command": "python3",
    "args": ["/home/your-username/dev/personal/gdb-mcp/gdb-mcp.py"]
    }
  }
}
```

### For VS Code Copilot

Add this configuration to your VS Code settings:

```json
{
  "mcp": {
    "inputs": [],
    "servers": {
      "gdb": {
        "command": "python3",
        "args": ["/home/your-username/dev/personal/gdb-mcp/gdb-mcp.py"]
      }
    }
  }
}
```

## Testing with Example Program

1. Compile the example program with debug symbols:
```bash
gcc -g example.c -o example
```

2. Use this prompt with your LLM client:

```
I have a binary at /path/to/example that I need to analyze. I don't have access to the source code. Please help me understand and debug this program using GDB.

1. Start a GDB session and load the binary
2. Use info functions to discover what functions are available
3. For each interesting function:
   - Disassemble it to understand its behavior
   - Set breakpoints at key instructions
   - Run the program and examine variables at breakpoints
4. When the program crashes or exhibits unexpected behavior:
   - Get a backtrace
   - Examine registers and variables
   - Help me understand what might be causing the issue

For each step:
- Explain what we're doing and why
- Show me the disassembly or variable values
- Help me interpret what we're seeing
- Suggest next steps based on our findings
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the GNU v3 License - see the LICENSE file for details.