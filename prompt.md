I have a binary at /home/smadi0x86wsl/dev/personal/gdb-mcp/example that I need to analyze. I don't have access to the source code. Please help me understand and debug this program using GDB through the MCP server.

Please help me:
1. Start a GDB session and load the binary
2. Use info functions to discover what functions are available
3. For each interesting function:
   - Disassemble it to understand its behavior
   - Set breakpoints at key instructions
   - Run the program and examine memory at breakpoints
4. When the program crashes or exhibits unexpected behavior:
   - Get a backtrace
   - Examine memory around the crash point
   - Disassemble the crashing function
   - Help me understand what might be causing the issue

For each step:
- Explain what we're doing and why
- Show me the disassembly or memory contents
- Help me interpret what we're seeing
- Suggest next steps based on our findings