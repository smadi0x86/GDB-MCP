from dataclasses import dataclass
from typing import Optional
import subprocess


@dataclass
class GdbSession:
    process: subprocess.Popen
    ready: bool = False
    target: Optional[str] = None
    working_dir: Optional[str] = None
    id: str = ""