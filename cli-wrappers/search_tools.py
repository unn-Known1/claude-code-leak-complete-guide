"""
Search Tools - Glob and Grep functionality

Based on Claude Code's search tools implementation.
"""

import os
import re
import fnmatch
from typing import List, Optional, Dict
from dataclasses import dataclass

from file_operations import RiskLevel


@dataclass
class SearchResult:
    """Result from a search operation"""
    path: str
    line_number: Optional[int] = None
    content: Optional[str] = None
    matches: Optional[List[str]] = None


class GlobTool:
    """
    File pattern matching tool.

    Based on Claude Code's GlobTool implementation.
    """

    def __init__(self):
        self.default_root = os.getcwd()

    def find(
        self,
        pattern: str,
        root: Optional[str] = None,
        recursive: bool = True,
        include_hidden: bool = False
    ) -> List[str]:
        """
        Find files matching a glob pattern.

        Args:
            pattern: Glob pattern (e.g., "**/*.py")
            root: Root directory to search
            recursive: Whether to search recursively
            include_hidden: Whether to include hidden files

        Returns:
            List of matching file paths
        """
        search_root = root or self.default_root
        matches = []

        # Handle recursive patterns
        if '**' in pattern:
            matches = self._glob_recursive(
                pattern, search_root, include_hidden
            )
        else:
            matches = self._glob_simple(
                pattern, search_root, include_hidden
            )

        return sorted(matches)

    def _glob_recursive(
        self,
        pattern: str,
        root: str,
        include_hidden: bool
    ) -> List[str]:
        """Handle recursive glob patterns"""
        matches = []

        # Split pattern at **
        parts = pattern.split('**')
        prefix = parts[0].rstrip('/')
        suffix = parts[1].lstrip('/') if len(parts) > 1 else ''

        search_path = os.path.join(root, prefix) if prefix else root

        if not os.path.exists(search_path):
            return []

        for dirpath, dirnames, filenames in os.walk(search_path):
            # Filter hidden directories if needed
            if not include_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]

            if suffix:
                for filename in fnmatch.filter(filenames, suffix):
                    full_path = os.path.join(dirpath, filename)
                    matches.append(full_path)
            else:
                for filename in filenames:
                    if include_hidden or not filename.startswith('.'):
                        full_path = os.path.join(dirpath, filename)
                        matches.append(full_path)

        return matches

    def _glob_simple(
        self,
        pattern: str,
        root: str,
        include_hidden: bool
    ) -> List[str]:
        """Handle simple glob patterns"""
        matches = []
        search_path = os.path.join(root, os.path.dirname(pattern))
        filename_pattern = os.path.basename(pattern)

        if not os.path.exists(search_path):
            return []

        for entry in os.listdir(search_path):
            if not include_hidden and entry.startswith('.'):
                continue

            if fnmatch.fnmatch(entry, filename_pattern):
                full_path = os.path.join(search_path, entry)
                matches.append(full_path)

        return matches


class GrepTool:
    """
    Content search tool.

    Based on Claude Code's GrepTool implementation.
    """

    def __init__(self):
        self.default_root = os.getcwd()

    def search(
        self,
        pattern: str,
        path: Optional[str] = None,
        file_type: Optional[str] = None,
        case_sensitive: bool = True,
        whole_word: bool = False,
        regex: bool = True,
        context_lines: int = 0
    ) -> List[SearchResult]:
        """
        Search for pattern in files.

        Args:
            pattern: Search pattern
            path: Path to search in
            file_type: File extension filter (e.g., "py", "js")
            case_sensitive: Case-sensitive search
            whole_word: Match whole words only
            regex: Treat pattern as regex
            context_lines: Number of context lines to include

        Returns:
            List of SearchResult objects
        """
        search_root = path or self.default_root
        results = []

        # Compile pattern
        flags = 0 if case_sensitive else re.IGNORECASE

        if regex:
            if whole_word:
                pattern = rf'\b{re.escape(pattern)}\b'
            compiled_pattern = re.compile(pattern, flags)
        else:
            if whole_word:
                pattern = rf'\b{re.escape(pattern)}\b'
            compiled_pattern = re.compile(pattern, flags)

        # Find files to search
        glob = GlobTool()
        search_pattern = f'**/*.{file_type}' if file_type else '**/*'
        files = glob.find(search_pattern, search_root)

        # Search in each file
        for filepath in files:
            file_results = self._search_file(
                filepath,
                compiled_pattern,
                context_lines
            )
            results.extend(file_results)

        return results

    def _search_file(
        self,
        filepath: str,
        pattern: re.Pattern,
        context_lines: int
    ) -> List[SearchResult]:
        """Search within a single file"""
        results = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                matches = pattern.findall(line)
                if matches:
                    results.append(SearchResult(
                        path=filepath,
                        line_number=i + 1,
                        content=line.rstrip('\n'),
                        matches=matches
                    ))

        except Exception:
            pass  # Skip files that can't be read

        return results

    def count(
        self,
        pattern: str,
        path: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> Dict[str, int]:
        """Count occurrences per file"""
        results = self.search(pattern, path, file_type)
        counts = {}

        for result in results:
            counts[result.path] = counts.get(result.path, 0) + 1

        return counts
