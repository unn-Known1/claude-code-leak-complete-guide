"""
CLI Tool Wrappers for Claude Code Functionality

This module provides reimplementations of Claude Code's core tools
based on the leaked source code analysis.
"""

__version__ = "1.0.0"

from .file_operations import (
    FileReadTool,
    FileWriteTool,
    FileEditTool,
    RiskLevel,
    PathTraversalProtection,
    SecurityError
)
from .shell_executor import (
    BashTool,
    PowerShellTool,
    REPLTool,
    CommandValidator,
    ShellResult
)
from .search_tools import (
    GlobTool,
    GrepTool,
    SearchResult
)
from .web_tools import (
    WebFetchTool,
    WebSearchTool,
    WebBrowserTool,
    URLValidator
)

__all__ = [
    # File operations
    'FileReadTool',
    'FileWriteTool',
    'FileEditTool',
    'RiskLevel',
    'PathTraversalProtection',
    'SecurityError',
    # Shell execution
    'BashTool',
    'PowerShellTool',
    'REPLTool',
    'CommandValidator',
    'ShellResult',
    # Search tools
    'GlobTool',
    'GrepTool',
    'SearchResult',
    # Web tools
    'WebFetchTool',
    'WebSearchTool',
    'WebBrowserTool',
    'URLValidator',
]
