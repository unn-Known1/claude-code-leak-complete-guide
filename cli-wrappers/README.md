# CLI Tool Wrappers for Claude Code

This directory contains CLI tool wrappers that replicate and extend Claude Code's core functionality based on the leaked source analysis.

## Available Tools

| Tool | Language | Description | Status |
|------|----------|-------------|--------|
| `file_operations.py` | Python | File read/write/edit operations | Stable |
| `shell_executor.py` | Python | Bash/PowerShell command execution | Stable |
| `search_tools.py` | Python | Glob and Grep functionality | Stable |
| `web_tools.py` | Python | WebFetch, WebSearch, WebBrowser | Beta |

## Installation

```bash
pip install -r requirements.txt
```

## Core Features

### Security Features (Based on Claude Code)

These wrappers include security measures discovered in the original Claude Code:

- **Path Traversal Protection**: Blocks URL-encoded, Unicode normalization, and backslash injection attacks
- **Risk Classification**: LOW, MEDIUM, HIGH risk levels for operations
- **Permission Modes**: `default`, `auto`, `bypass`, `yolo` permission levels
- **Command Validation**: Whitelist-based command validation for shell operations

## Usage Examples

### File Operations

```python
from file_operations import FileReadTool, FileWriteTool, FileEditTool, RiskLevel

# Read a file
reader = FileReadTool()
result = reader.read("path/to/file.txt")
if result.success:
    print(result.content)

# Write a file
writer = FileWriteTool()
result = writer.write("output.txt", "Hello, World!")
print(f"Written {result.bytes_written} bytes")

# Edit a file
editor = FileEditTool()
result = editor.edit("file.txt", old_text="old", new_text="new")
```

### Shell Execution

```python
from shell_executor import BashTool, PowerShellTool, REPLTool

# Execute bash command
bash = BashTool(timeout=30)
result = bash.execute("ls -la")
print(result.stdout)

# Execute PowerShell
ps = PowerShellTool()
result = ps.execute("Get-Process")

# Execute in REPL
repl = REPLTool()
result = repl.execute("print('Hello')", interpreter="python")
```

### Search Tools

```python
from search_tools import GlobTool, GrepTool

# Find files
glob = GlobTool()
files = glob.find("**/*.py", root="/project")

# Search content
grep = GrepTool()
results = grep.search(r"def\s+\w+", path="/project", file_type="py")
```

## License

MIT License - See root LICENSE file for details.
