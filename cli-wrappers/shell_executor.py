"""
Shell Execution Tools - Based on Claude Code's shell execution system

This module replicates BashTool, PowerShellTool, and REPLTool
with the security features discovered in the Claude Code leak.
"""

import subprocess
import shlex
import os
import time
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

from file_operations import RiskLevel


# Whitelist of allowed commands (basic safety measure)
ALLOWED_COMMANDS = {
    'ls', 'cat', 'echo', 'pwd', 'cd', 'mkdir', 'touch', 'cp', 'mv', 'rm',
    'grep', 'find', 'awk', 'sed', 'sort', 'uniq', 'head', 'tail', 'wc',
    'git', 'npm', 'yarn', 'pnpm', 'pip', 'python', 'python3', 'node',
    'cargo', 'rustc', 'go', 'docker', 'curl', 'wget', 'tar', 'gzip',
    'zip', 'unzip', 'chmod', 'chown', 'sudo',
}

# Dangerous patterns to block
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',  # Recursive root delete
    r'rm\s+-rf\s+\*',  # Recursive delete all
    r'mkfs\.',  # Filesystem creation
    r'format\s+',  # Disk format
    r'>\s*/dev/',  # Device writing
    r'\|\s*sh\s*$',  # Pipe to shell
    r';\s*sh\s*$',  # Shell execution
    r'`.*`',  # Command substitution
    r'\$\(.*\)',  # Command substitution
]


@dataclass
class ShellResult:
    """Result of a shell command execution"""
    success: bool
    stdout: str
    stderr: str
    returncode: int
    execution_time: float
    risk_level: RiskLevel


class CommandValidationError(Exception):
    """Raised when a command fails validation"""
    pass


class CommandValidator:
    """Validates commands for safety based on Claude Code's approach"""

    @classmethod
    def validate(cls, command: str, allowed_dirs: Optional[List[str]] = None) -> Tuple[bool, str]:
        """
        Validate a command for safety.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for dangerous patterns
        for pattern in DANGEROUS_PATTERNS:
            import re
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Dangerous pattern detected: {pattern}"

        # Parse command
        try:
            parts = shlex.split(command)
            if not parts:
                return False, "Empty command"

            base_cmd = os.path.basename(parts[0])

            # Check whitelist for basic commands
            if base_cmd not in ALLOWED_COMMANDS:
                # Allow absolute paths
                if not parts[0].startswith('/'):
                    return False, f"Command not in whitelist: {base_cmd}"
        except ValueError as e:
            return False, f"Invalid command syntax: {e}"

        # Check directory restrictions
        if allowed_dirs:
            for part in parts:
                if part.startswith('/') and not any(
                    part.startswith(d) for d in allowed_dirs
                ):
                    return False, f"Path outside allowed directories: {part}"

        return True, ""


class BashTool:
    """
    Bash command execution tool with security controls.

    Based on Claude Code's BashTool implementation.
    """

    def __init__(
        self,
        timeout: int = 30,
        allowed_dirs: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None
    ):
        self.timeout = timeout
        self.allowed_dirs = allowed_dirs or []
        self.env = env or {}

    def execute(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: Optional[int] = None,
        check: bool = False
    ) -> ShellResult:
        """
        Execute a bash command with security validation.

        Args:
            command: Command to execute
            cwd: Working directory
            timeout: Timeout in seconds (overrides default)
            check: Raise exception on non-zero exit

        Returns:
            ShellResult with output and status
        """
        start_time = time.time()

        # Validate command
        is_valid, error_msg = CommandValidator.validate(
            command, self.allowed_dirs
        )
        if not is_valid:
            return ShellResult(
                success=False,
                stdout="",
                stderr=error_msg,
                returncode=1,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.HIGH
            )

        # Prepare environment
        exec_env = os.environ.copy()
        exec_env.update(self.env)

        # Prepare timeout
        exec_timeout = timeout or self.timeout

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                env=exec_env,
                capture_output=True,
                text=True,
                timeout=exec_timeout,
                check=check
            )

            return ShellResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )

        except subprocess.TimeoutExpired:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Command timed out after {exec_timeout} seconds",
                returncode=124,
                execution_time=exec_timeout,
                risk_level=RiskLevel.LOW
            )
        except Exception as e:
            return ShellResult(
                success=False,
                stdout="",
                stderr=str(e),
                returncode=1,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )

    def interactive(
        self,
        command: str,
        input_data: Optional[str] = None
    ) -> ShellResult:
        """Execute command with interactive input"""
        start_time = time.time()

        is_valid, error_msg = CommandValidator.validate(
            command, self.allowed_dirs
        )
        if not is_valid:
            return ShellResult(
                success=False,
                stdout="",
                stderr=error_msg,
                returncode=1,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.HIGH
            )

        try:
            result = subprocess.run(
                command,
                shell=True,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            return ShellResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )

        except Exception as e:
            return ShellResult(
                success=False,
                stdout="",
                stderr=str(e),
                returncode=1,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )


class PowerShellTool:
    """
    PowerShell command execution tool for Windows environments.

    Based on Claude Code's PowerShellTool implementation.
    """

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> ShellResult:
        """Execute a PowerShell command"""
        start_time = time.time()
        exec_timeout = timeout or self.timeout

        try:
            result = subprocess.run(
                ['powershell', '-Command', command],
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=exec_timeout
            )

            return ShellResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )

        except subprocess.TimeoutExpired:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Command timed out after {exec_timeout} seconds",
                returncode=124,
                execution_time=exec_timeout,
                risk_level=RiskLevel.LOW
            )
        except Exception as e:
            return ShellResult(
                success=False,
                stdout="",
                stderr=str(e),
                returncode=1,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )


class REPLTool:
    """
    Interactive REPL execution tool.

    Based on Claude Code's REPLTool implementation.
    """

    SUPPORTED_REPLS = {
        'python': ['python', 'python3', 'python3.11', 'python3.12'],
        'node': ['node', 'nodejs'],
        'bash': ['bash', 'sh', 'zsh'],
        'ruby': ['ruby', 'irb'],
        'psql': ['psql'],
        'mysql': ['mysql'],
    }

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute(
        self,
        code: str,
        interpreter: str = 'python',
        timeout: Optional[int] = None
    ) -> ShellResult:
        """
        Execute code in a REPL interpreter.

        Args:
            code: Code to execute
            interpreter: REPL interpreter to use
            timeout: Timeout in seconds

        Returns:
            ShellResult with output
        """
        start_time = time.time()
        exec_timeout = timeout or self.timeout

        # Validate interpreter
        valid_commands = self.SUPPORTED_REPLS.get(interpreter.lower(), [])
        if not valid_commands:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Unsupported interpreter: {interpreter}",
                returncode=1,
                execution_time=0,
                risk_level=RiskLevel.LOW
            )

        try:
            result = subprocess.run(
                [valid_commands[0], '-c', code],
                capture_output=True,
                text=True,
                timeout=exec_timeout
            )

            return ShellResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )

        except subprocess.TimeoutExpired:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Execution timed out after {exec_timeout} seconds",
                returncode=124,
                execution_time=exec_timeout,
                risk_level=RiskLevel.LOW
            )
        except Exception as e:
            return ShellResult(
                success=False,
                stdout="",
                stderr=str(e),
                returncode=1,
                execution_time=time.time() - start_time,
                risk_level=RiskLevel.MEDIUM
            )
