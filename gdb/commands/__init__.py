from typing import Dict, Optional, List
import os
import re
from ..core.gdb import (
    start_gdb,
    exec_gdb_command,
    get_session,
    remove_session,
    active_sessions
)
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("gdb-mcp")


def gdb_start(gdb_path: str = "gdb", working_dir: Optional[str] = None) -> Dict:
    """
    Start a new GDB session.
    """
    try:
        session_id, output = start_gdb(gdb_path, working_dir)
        return {"session_id": session_id, "output": output}
    except Exception as e:
        return {"error": str(e)}


def gdb_load(session_id: str, program: str, arguments: Optional[List[str]] = None) -> Dict:
    """
    Load a program into GDB.
    """
    try:
        session = get_session(session_id)
        if not session:
            return {"error": "Invalid session ID"}

        # Normalize path if working directory is set
        normalized_path = program
        if session.working_dir and not os.path.isabs(program):
            normalized_path = os.path.join(session.working_dir, program)

        # Update session target
        session.target = normalized_path

        # Load program
        load_output = exec_gdb_command(session_id, f'file "{normalized_path}"')

        # Set arguments if provided
        args_output = ""
        if arguments:
            args_command = f'set args {" ".join(arguments)}'
            args_output = exec_gdb_command(session_id, args_command)

        # Run the program
        run_output = exec_gdb_command(session_id, "run")

        return {
            "output": f"Program loaded: {normalized_path}\n\nOutput:\n{load_output}{args_output}\n\nRun output:\n{run_output}"
        }
    except Exception as e:
        return {"error": str(e)}

def gdb_run(session_id: str) -> Dict:
    """
    Run the loaded program.
    """
    try:
        output = exec_gdb_command(session_id, "run")
        return {"output": f"Running program\n\nOutput:\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_command(session_id: str, command: str) -> Dict:
    """
    Execute a command in an existing GDB session.
    """
    try:
        output = exec_gdb_command(session_id, command)
        return {"output": f"Command: {command}\n\nOutput:\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_attach(session_id: str, pid: int) -> Dict:
    """
    Attach to a running process.
    """
    try:
        output = exec_gdb_command(session_id, f"attach {pid}")
        return {"output": f"Attached to process {pid}\n\nOutput:\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_load_core(session_id: str, program: str, core_path: str) -> Dict:
    """
    Load a core dump file.
    """
    try:
        # Load program
        file_output = exec_gdb_command(session_id, f'file "{program}"')

        # Load core file
        core_output = exec_gdb_command(session_id, f'core-file "{core_path}"')

        # Get backtrace
        backtrace_output = exec_gdb_command(session_id, "backtrace")

        return {
            "output": f"Core file loaded: {core_path}\n\nOutput:\n{file_output}\n{core_output}\n\nBacktrace:\n{backtrace_output}"
        }
    except Exception as e:
        return {"error": str(e)}


def gdb_set_breakpoint(session_id: str, location: str, condition: Optional[str] = None) -> Dict:
    """
    Set a breakpoint.
    """
    try:
        # Set breakpoint
        command = f"break {location}"
        output = exec_gdb_command(session_id, command)

        # Set condition if provided
        condition_output = ""
        if condition:
            # Extract breakpoint number from output
            match = re.search(r"Breakpoint (\d+)", output)
            if match:
                bp_num = match.group(1)
                condition_command = f"condition {bp_num} {condition}"
                condition_output = exec_gdb_command(session_id, condition_command)

        return {
            "output": f"Breakpoint set at: {location}{f' with condition: {condition}' if condition else ''}\n\nOutput:\n{output}{condition_output}"
        }
    except Exception as e:
        return {"error": str(e)}


def gdb_continue(session_id: str) -> Dict:
    """
    Continue program execution.
    """
    try:
        output = exec_gdb_command(session_id, "continue")
        return {"output": f"Continued execution\n\nOutput:\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_step(session_id: str, instructions: bool = False) -> Dict:
    """
    Step program execution.
    """
    try:
        command = "stepi" if instructions else "step"
        output = exec_gdb_command(session_id, command)
        return {"output": f"Stepped {'instruction' if instructions else 'line'}\n\nOutput:\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_next(session_id: str, instructions: bool = False) -> Dict:
    """
    Step over function calls.
    """
    try:
        command = "nexti" if instructions else "next"
        output = exec_gdb_command(session_id, command)
        return {"output": f"Stepped over {'instruction' if instructions else 'function call'}\n\nOutput:\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_finish(session_id: str) -> Dict:
    """
    Execute until the current function returns.
    """
    try:
        output = exec_gdb_command(session_id, "finish")
        return {"output": f"Finished current function\n\nOutput:\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_backtrace(session_id: str, full: bool = False, limit: Optional[int] = None) -> Dict:
    """
    Show call stack.
    """
    try:
        command = "backtrace full" if full else "backtrace"
        if limit is not None:
            command += f" {limit}"
        output = exec_gdb_command(session_id, command)
        return {"output": f"Backtrace{' (full)' if full else ''}{f' (limit: {limit})' if limit else ''}:\n\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_print(session_id: str, expression: str) -> Dict:
    """
    Print value of expression.
    """
    try:
        output = exec_gdb_command(session_id, f"print {expression}")
        return {"output": f"Print {expression}:\n\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_disassemble(
    session_id: str,
    location: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    count: Optional[int] = None
) -> Dict:
    """
    Disassemble program code.
    """
    try:
        # Build the command
        command = "disassemble"
        if location:
            command += f" {location}"
        elif start:
            command += f" {start}"
            if end:
                command += f",{end}"
            elif count:
                command += f",+{count}"

        output = exec_gdb_command(session_id, command)
        return {
            "output": f"Disassembly{f' of {location}' if location else ''}{f' from {start}' if start else ''}{f' to {end}' if end else ''}{f' ({count} instructions)' if count else ''}:\n\n{output}"
        }
    except Exception as e:
        return {"error": str(e)}


def gdb_info_registers(session_id: str, register: Optional[str] = None) -> Dict:
    """
    Display registers.
    """
    try:
        command = f"info registers {register}" if register else "info registers"
        output = exec_gdb_command(session_id, command)
        return {"output": f"Register info{f' for {register}' if register else ''}:\n\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_info_functions(session_id: str, pattern: Optional[str] = None) -> Dict:
    """
    List all functions in the program, optionally filtered by a pattern.
    """
    try:
        command = "info functions"
        if pattern:
            command += f" {pattern}"
        output = exec_gdb_command(session_id, command)
        return {"output": f"Functions in program{f' matching {pattern}' if pattern else ''}:\n\n{output}"}
    except Exception as e:
        return {"error": str(e)}


def gdb_list_sessions() -> Dict:
    """
    List all active GDB sessions.
    """
    return {
        "sessions": [
            {
                "session_id": session_id,
                "working_dir": session.working_dir,
                "target": session.target,
            }
            for session_id, session in active_sessions.items()
        ]
    }


def gdb_terminate(session_id: str) -> Dict:
    """
    Terminate an existing GDB session.
    """
    try:
        session = get_session(session_id)
        if not session:
            return {"error": "Invalid session ID"}

        # Try to quit gracefully
        try:
            exec_gdb_command(session_id, "quit")
        except:
            pass

        # Force kill if still running
        if session.process.poll() is None:
            session.process.kill()

        remove_session(session_id)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}