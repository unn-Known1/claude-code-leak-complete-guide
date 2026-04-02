# Permission System

## Overview

Claude Code implements a four-tier permission system that controls what operations can be performed. This document details the permission modes and bypass mechanisms discovered in the leaked source code.

## Permission Modes

Claude Code supports four permission modes, each with increasing levels of access:

### Mode Comparison

| Mode | File Write | Shell Execute | Dangerous Ops | Approval Required |
|------|-----------|---------------|---------------|-------------------|
| `default` | Yes | Limited | No | Yes |
| `auto` | Yes | Yes | No | No |
| `bypass` | Yes | Yes | Yes (limited) | No |
| `yolo` | Yes | Yes | Yes | No |

### 1. Default Mode

**Purpose**: Safe, production-ready operation

**Characteristics**:
- File operations allowed
- Shell commands restricted to whitelist
- No dangerous operations
- Always prompts for write operations
- Respects git protection (.gitignore)

**Allowed Shell Commands**:

```bash
# File operations
ls, cat, echo, pwd, cd, mkdir, touch, cp, mv, rm,
grep, find, awk, sed, sort, uniq, head, tail, wc

# Version control
git, npm, yarn, pnpm, pip, python, python3, node

# Building
cargo, rustc, go, docker, make, cmake
```

**Blocked Patterns**:

```bash
rm -rf /           # Root deletion
mkfs.*             # Filesystem creation
format             # Disk format
> /dev/sd*         # Direct device write
| sh                # Pipe to shell
`command`          # Command substitution
```

### 2. Auto Mode

**Purpose**: Streamlined development without prompts

**Characteristics**:
- File operations allowed
- All whitelisted shell commands allowed
- No dangerous operations
- No approval prompts
- Automatic risk assessment

**Configuration**:

```bash
CLAUDE_CODE_PERMISSION_MODE=auto
```

### 3. Bypass Mode

**Purpose**: Advanced usage requiring dangerous operations

**Characteristics**:
- File operations allowed
- All shell commands allowed (with logging)
- Dangerous operations allowed (logged)
- No prompts
- Enhanced audit trail

**Environment Variable**:

```bash
CLAUDE_CODE_PERMISSION_MODE=bypass
```

**Audit Logging**:

```json
{
  "timestamp": "2026-04-01T12:00:00Z",
  "operation": "dangerous_shell",
  "command": "rm -rf node_modules",
  "mode": "bypass",
  "approved": true
}
```

### 4. Yolo Mode

**Purpose**: Unrestricted operation (use with caution)

**Characteristics**:
- ALL file operations allowed
- ALL shell commands allowed
- NO safety checks
- NO logging
- NO confirmation

**Environment Variable**:

```bash
CLAUDE_CODE_PERMISSION_MODE=yolo
```

**Warning**: This mode bypasses all security measures. Use only in controlled environments.

## Permission Configuration

### Setting Mode

```bash
# Via environment
export CLAUDE_CODE_PERMISSION_MODE=auto

# Via config file (~/.claude/config.json)
{
  "permissionMode": "auto"
}

# Via CLI flag
claude --permission=auto "fix the bug"
```

### Per-Project Configuration

Create `.claude/settings.json` in project root:

```json
{
  "permissions": {
    "mode": "default",
    "allowedPaths": ["./src", "./tests"],
    "blockedCommands": ["docker system prune"],
    "maxShellTimeout": 300
  }
}
```

### Command-Specific Overrides

```bash
# Single command with different mode
claude --permission=bypass "clean up disk space"

# Temporary elevation
claude-elevate "run dangerous operation"
```

## Risk Assessment

### Automatic Risk Classification

```typescript
interface Operation {
  type: 'file' | 'shell' | 'network';
  action: string;
  target?: string;
}

function assessRisk(op: Operation): RiskLevel {
  let score = 0;

  // Operation type
  if (op.type === 'shell') score += 2;
  if (op.type === 'network') score += 1;

  // Action danger
  if (['delete', 'rm', 'drop'].includes(op.action)) score += 3;
  if (['write', 'create'].includes(op.action)) score += 1;

  // Target location
  if (op.target?.includes('.git')) score += 2;
  if (op.target?.includes('/etc')) score += 3;
  if (op.target?.includes('node_modules')) score -= 1;

  // Classify
  if (score >= 5) return 'HIGH';
  if (score >= 2) return 'MEDIUM';
  return 'LOW';
}
```

### Mode-Specific Enforcement

| Risk Level | Default | Auto | Bypass | Yolo |
|------------|---------|------|--------|------|
| LOW | Allow | Allow | Allow | Allow |
| MEDIUM | Prompt | Allow | Allow | Allow |
| HIGH | Block | Prompt | Allow | Allow |

## Security Implications

### Default Mode

**Pros**:
- Safest option
- Prevents accidental data loss
- Protects system files
- Production-safe

**Cons**:
- Frequent prompts
- Limited functionality
- May block legitimate operations

### Yolo Mode

**Pros**:
- Maximum flexibility
- No interruptions
- Full system access

**Cons**:
- No protection
- Potential for data loss
- No audit trail
- Dangerous

## Best Practices

### Development

Use `auto` mode for active development with frequent file changes.

```bash
export CLAUDE_CODE_PERMISSION_MODE=auto
```

### Code Review

Use `default` mode for reviewing code without modifications.

```bash
claude review --permission=default "check my code"
```

### Production Debugging

Use `bypass` mode with caution for production issues.

```bash
export CLAUDE_CODE_PERMISSION_MODE=bypass
claude debug "investigate production issue"
```

### CI/CD

Use `default` mode in CI environments.

```yaml
# GitHub Actions
- run: claude --permission=default "run tests"
  env:
    CLAUDE_CODE_PERMISSION_MODE: default
```

## Audit Trail

### Viewing Permission Denials

```bash
# Show recent denials
claude logs --filter=permission_denied

# Show all security events
claude logs --filter=security
```

### Exporting Audit Log

```bash
claude audit export --format=json --output=audit.json
```

## Environment Variables Summary

| Variable | Purpose | Values |
|----------|---------|--------|
| `CLAUDE_CODE_PERMISSION_MODE` | Set default mode | `default`, `auto`, `bypass`, `yolo` |
| `CLAUDE_CODE_ALLOWED_PATHS` | Restrict file access | Colon-separated paths |
| `CLAUDE_CODE_BLOCKED_COMMANDS` | Block specific commands | Comma-separated commands |
| `CLAUDE_CODE_MAX_SHELL_TIMEOUT` | Shell command timeout | Seconds |
