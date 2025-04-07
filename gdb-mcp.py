#!/usr/bin/env python3

"""
GDB MCP Server - An MCP server for GDB debugging.
"""
import sys
from gdb import run_server

def main():
    try:
        print("Starting GDB MCP server...", file=sys.stderr)
        run_server()
    except KeyboardInterrupt:
        print("\nShutting down GDB MCP server...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()