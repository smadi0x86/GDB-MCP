import os
import uuid
import subprocess
from typing import Dict, Optional, Tuple, List
from ..models.session import GdbSession

# Global session storage
active_sessions: Dict[str, GdbSession] = {}


def start_gdb(gdb_path: str, working_dir: Optional[str]) -> Tuple[str, str]:
    """
    Start a new GDB session.
    """
    session_id = str(uuid.uuid4())
    process = subprocess.Popen(
        [gdb_path, "--interpreter=mi"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=working_dir or os.getcwd(),
    )

    if process.stdout is None:
        raise ValueError("Failed to initialize GDB stdout stream")

    # Wait for GDB readiness
    output = []
    while True:
        line = process.stdout.readline()
        if not line:
            break
        output.append(line)
        if "(gdb)" in line:
            break

    session = GdbSession(process, working_dir=working_dir, id=session_id)
    active_sessions[session_id] = session
    return session_id, "".join(output)


def exec_gdb_command(session_id: str, command: str) -> str:
    """
    Execute a command in an existing GDB session.
    """
    session = active_sessions.get(session_id)
    if not session:
        raise ValueError("Invalid session ID")

    if session.process.stdin is None or session.process.stdout is None:
        raise ValueError("Session process streams are not available")

    session.process.stdin.write(f"{command}\n")
    session.process.stdin.flush()

    output = []
    while True:
        line = session.process.stdout.readline()
        if not line:
            break
        output.append(line)
        if "(gdb)" in line or "^done" in line or "^error" in line:
            break

    return "".join(output)


def get_session(session_id: str) -> Optional[GdbSession]:
    """
    Get a GDB session by ID.
    """
    return active_sessions.get(session_id)


def remove_session(session_id: str) -> None:
    """
    Remove a GDB session.
    """
    if session_id in active_sessions:
        del active_sessions[session_id]
