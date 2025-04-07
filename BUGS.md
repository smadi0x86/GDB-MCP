# Known Bugs

## GDB Machine Interface (MI) Output Parsing Issues

### `info functions` Command
- **Status**: Disabled
- **Description**: The command fails to properly parse GDB MI output format
- **Symptoms**:
  - Returns program execution messages instead of function list
  - Empty output even when functions exist
  - Incorrect handling of MI output markers
- **Root Cause**: Improper parsing of GDB MI output format and program state management

### `disassemble` Command
- **Status**: Disabled
- **Description**: Similar MI output parsing issues as info functions
- **Symptoms**:
  - Returns program startup messages instead of disassembly
  - Fails to properly extract assembly instructions
  - Incorrect handling of MI output format
- **Root Cause**: Same as info functions - MI output parsing issues

## Session Management
- **Status**: Active
- **Description**: Session cleanup on program crash may not be complete
- **Symptoms**:
  - Orphaned GDB processes may remain after session termination
  - Memory leaks in long-running sessions
- **Workaround**: Manually kill any remaining GDB processes

## Error Handling
- **Status**: Active
- **Description**: Some error conditions may not be properly propagated
- **Symptoms**:
  - Generic error messages instead of specific GDB errors
  - Incomplete error information in some cases
- **Workaround**: Check GDB output directly for detailed error messages