"""
File Operations Tool - Based on Claude Code's file operations system

This module replicates the FileReadTool, FileWriteTool, and FileEditTool
from Claude Code, with security enhancements discovered in the leak.
"""

import os
import re
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Risk classification for file operations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class FileOperationResult:
    """Result of a file operation"""
    success: bool
    content: Optional[str] = None
    bytes_written: Optional[int] = None
    error: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.LOW


class SecurityError(Exception):
    """Raised when a security violation is detected"""
    pass


class PathTraversalProtection:
    """Prevents path traversal attacks discovered in Claude Code's security review"""

    BLOCKED_PATTERNS = [
        r'\.\.',  # Double dots
        r'%2e%2e',  # URL encoded dots
        r'%252e',  # Double URL encoded
        r'\x2e\x2e',  # Hex encoded
        r'\u002e\u002e',  # Unicode encoded
        r'^/',  # Absolute paths
        r'^~',  # Home directory
        r'\\\\',  # Windows backslash injection
    ]

    @classmethod
    def is_safe(cls, path: str) -> bool:
        """Check if path is safe from traversal attacks"""
        normalized = os.path.normpath(path)

        for pattern in cls.BLOCKED_PATTERNS:
            if re.search(pattern, path, re.IGNORECASE):
                return False

        # Check for Unicode normalization exploits
        if normalized != path:
            return False

        return True

    @classmethod
    def validate(cls, path: str, base_dir: Optional[str] = None) -> str:
        """Validate and return safe path, raising exception if unsafe"""
        if not cls.is_safe(path):
            raise SecurityError(f"Path traversal attempt detected: {path}")

        if base_dir:
            resolved = os.path.abspath(os.path.join(base_dir, path))
            if not resolved.startswith(os.path.abspath(base_dir)):
                raise SecurityError(f"Path escapes base directory: {path}")
            return resolved

        return os.path.abspath(path)


class FileReadTool:
    """
    File reading tool with security checks.

    Based on Claude Code's FileReadTool implementation.
    """

    def __init__(self, max_file_size: int = 10 * 1024 * 1024):
        self.max_file_size = max_file_size

    def read(self, path: str, base_dir: Optional[str] = None) -> FileOperationResult:
        """
        Read contents of a file with security validation.

        Args:
            path: Path to the file to read
            base_dir: Optional base directory for relative path resolution

        Returns:
            FileOperationResult with content or error
        """
        try:
            safe_path = PathTraversalProtection.validate(path, base_dir)

            # Check file size
            file_size = os.path.getsize(safe_path)
            if file_size > self.max_file_size:
                return FileOperationResult(
                    success=False,
                    error=f"File too large: {file_size} bytes (max: {self.max_file_size})",
                    risk_level=RiskLevel.MEDIUM
                )

            with open(safe_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return FileOperationResult(
                success=True,
                content=content,
                risk_level=RiskLevel.LOW
            )

        except FileNotFoundError:
            return FileOperationResult(
                success=False,
                error=f"File not found: {path}",
                risk_level=RiskLevel.LOW
            )
        except SecurityError as e:
            return FileOperationResult(
                success=False,
                error=str(e),
                risk_level=RiskLevel.HIGH
            )
        except Exception as e:
            return FileOperationResult(
                success=False,
                error=f"Error reading file: {str(e)}",
                risk_level=RiskLevel.MEDIUM
            )

    def read_lines(
        self,
        path: str,
        offset: int = 0,
        limit: Optional[int] = None,
        base_dir: Optional[str] = None
    ) -> FileOperationResult:
        """Read specific lines from a file"""
        result = self.read(path, base_dir)
        if not result.success:
            return result

        lines = result.content.split('\n')
        if offset > 0:
            lines = lines[offset:]
        if limit:
            lines = lines[:limit]

        return FileOperationResult(
            success=True,
            content='\n'.join(lines),
            risk_level=RiskLevel.LOW
        )


class FileWriteTool:
    """
    File writing tool with backup and validation.

    Based on Claude Code's FileWriteTool implementation.
    """

    def __init__(self, create_backups: bool = True):
        self.create_backups = create_backups

    def write(
        self,
        path: str,
        content: str,
        base_dir: Optional[str] = None,
        create_dirs: bool = True
    ) -> FileOperationResult:
        """
        Write content to a file with optional backup.

        Args:
            path: Path to write to
            content: Content to write
            base_dir: Optional base directory
            create_dirs: Whether to create parent directories

        Returns:
            FileOperationResult with success status
        """
        try:
            safe_path = PathTraversalProtection.validate(path, base_dir)

            # Create parent directories if needed
            if create_dirs:
                os.makedirs(os.path.dirname(safe_path) or '.', exist_ok=True)

            # Create backup if file exists
            if self.create_backups and os.path.exists(safe_path):
                backup_path = f"{safe_path}.backup"
                with open(safe_path, 'r') as src:
                    with open(backup_path, 'w') as dst:
                        dst.write(src.read())

            # Write content
            with open(safe_path, 'w', encoding='utf-8') as f:
                bytes_written = f.write(content)

            return FileOperationResult(
                success=True,
                bytes_written=bytes_written,
                risk_level=RiskLevel.MEDIUM
            )

        except SecurityError as e:
            return FileOperationResult(
                success=False,
                error=str(e),
                risk_level=RiskLevel.HIGH
            )
        except Exception as e:
            return FileOperationResult(
                success=False,
                error=f"Error writing file: {str(e)}",
                risk_level=RiskLevel.MEDIUM
            )


class FileEditTool:
    """
    Pattern-based file editing tool.

    Based on Claude Code's FileEditTool implementation.
    """

    def __init__(self, strict: bool = True):
        self.strict = strict

    def edit(
        self,
        path: str,
        old_text: str,
        new_text: str,
        base_dir: Optional[str] = None,
        count: int = 1
    ) -> FileOperationResult:
        """
        Replace text in a file using exact string matching.

        Args:
            path: Path to the file
            old_text: Text to replace
            new_text: Replacement text
            base_dir: Optional base directory
            count: Number of replacements (default 1)

        Returns:
            FileOperationResult with success status
        """
        try:
            safe_path = PathTraversalProtection.validate(path, base_dir)

            # Read current content
            with open(safe_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if old_text exists
            if self.strict and old_text not in content:
                return FileOperationResult(
                    success=False,
                    error=f"Text not found in file: {old_text[:50]}...",
                    risk_level=RiskLevel.LOW
                )

            # Perform replacement
            new_content = content.replace(old_text, new_text, count)

            # Write back
            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return FileOperationResult(
                success=True,
                bytes_written=len(new_content),
                risk_level=RiskLevel.MEDIUM
            )

        except SecurityError as e:
            return FileOperationResult(
                success=False,
                error=str(e),
                risk_level=RiskLevel.HIGH
            )
        except Exception as e:
            return FileOperationResult(
                success=False,
                error=f"Error editing file: {str(e)}",
                risk_level=RiskLevel.MEDIUM
            )

    def insert(
        self,
        path: str,
        text: str,
        after_line: Optional[int] = None,
        before_line: Optional[int] = None,
        base_dir: Optional[str] = None
    ) -> FileOperationResult:
        """Insert text at specific line position"""
        try:
            safe_path = PathTraversalProtection.validate(path, base_dir)

            with open(safe_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if after_line is not None:
                insert_pos = after_line + 1
            elif before_line is not None:
                insert_pos = before_line
            else:
                insert_pos = len(lines)

            lines.insert(insert_pos, text + '\n')

            with open(safe_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            return FileOperationResult(
                success=True,
                risk_level=RiskLevel.MEDIUM
            )

        except Exception as e:
            return FileOperationResult(
                success=False,
                error=str(e),
                risk_level=RiskLevel.MEDIUM
            )
