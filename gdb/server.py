from mcp.server.fastmcp import FastMCP
from .commands import (
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
)

# Registry of all available commands
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

def create_server() -> FastMCP:
    mcp = FastMCP("gdb-mcp")

    # Register all GDB commands as MCP tools
    for command in GDB_COMMANDS:
        mcp.tool()(command)

    return mcp


def run_server():
    mcp = create_server()
    mcp.run()  # Runs on stdio by default