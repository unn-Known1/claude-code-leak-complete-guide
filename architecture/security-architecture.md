# Security Architecture

## Overview

Claude Code implements a comprehensive security architecture discovered in the leaked source code. This document details the security mechanisms, path traversal protection, and risk classification system.

## Security Layers

### 1. Path Traversal Protection

Claude Code uses multiple layers of path validation to prevent directory traversal attacks.

#### Attack Vectors Blocked

| Attack Type | Pattern | Protection |
|-------------|---------|------------|
| Standard traversal | `../` | Normalization check |
| URL-encoded | `%2e%2e` | Pattern matching |
| Double URL-encoded | `%252e` | Multiple decode checks |
| Hex-encoded | `\x2e\x2e` | Character code validation |
| Unicode | `\u002e` | Normalization verification |
| Backslash injection | `\\` | Platform-specific handling |

#### Implementation

```typescript
class PathTraversalProtection {
  static isSafe(path: string): boolean {
    // Normalize and check
    const normalized = path.normalize('NFC');

    // Check for dangerous patterns
    const patterns = [
      /\.\./,           // Double dots
      /%2e%2e/i,        // URL encoded
      /%252e/i,         // Double URL encoded
      /\x2e\x2e/,       // Hex encoded
      /\u002e\u002e/,   // Unicode
    ];

    for (const pattern of patterns) {
      if (pattern.test(path)) return false;
    }

    // Verify normalization didn't change path
    return normalized === path;
  }

  static validate(path: string, baseDir?: string): string {
    if (!this.isSafe(path)) {
      throw new SecurityError(`Path traversal attempt: ${path}`);
    }

    if (baseDir) {
      const resolved = resolve(baseDir, path);
      if (!resolved.startsWith(resolve(baseDir))) {
        throw new SecurityError('Path escapes base directory');
      }
      return resolved;
    }

    return resolve(path);
  }
}
```

### 2. Risk Classification

Every operation is classified into risk levels:

#### Risk Levels

| Level | Description | Example Operations | Default Action |
|-------|-------------|-------------------|---------------|
| LOW | Read-only, safe operations | File read, glob, grep | Allow |
| MEDIUM | Modifies state, needs caution | File write, shell | Prompt or allow |
| HIGH | System-level changes | rm -rf, git reset | Require approval |

#### Classification Factors

```typescript
function classifyRisk(operation: Operation): RiskLevel {
  let risk = RiskLevel.LOW;

  // File operations
  if (operation.type === 'file.delete') risk = RiskLevel.HIGH;
  if (operation.type === 'file.write') risk = RiskLevel.MEDIUM;

  // Shell commands
  if (operation.type === 'shell.execute') {
    if (containsDangerousPatterns(operation.command)) {
      risk = RiskLevel.HIGH;
    } else {
      risk = RiskLevel.MEDIUM;
    }
  }

  // Web operations
  if (operation.type === 'web.fetch') risk = RiskLevel.MEDIUM;

  return risk;
}
```

### 3. Command Validation

Shell commands are validated against a whitelist:

#### Allowed Commands (Partial List)

```
ls, cat, echo, pwd, cd, mkdir, touch, cp, mv, rm,
grep, find, awk, sed, sort, uniq, head, tail, wc,
git, npm, yarn, pnpm, pip, python, python3, node,
cargo, rustc, go, docker, curl, wget, tar, gzip,
chmod, chown
```

#### Dangerous Pattern Detection

```typescript
const DANGEROUS_PATTERNS = [
  /rm\s+-rf\s+\//,        // Root deletion
  /mkfs\./,               // Filesystem creation
  /format\s+/,            // Disk format
  />\s*\/dev\//,          // Device writing
  /\|\s*sh\s*$/,          // Pipe to shell
  /;\s*sh\s*$/,           // Shell execution
  /`.*`/,                 // Command substitution
  /\$\(.*\)/,            // Command substitution
];

function containsDangerousPatterns(command: string): boolean {
  return DANGEROUS_PATTERNS.some(pattern =>
    pattern.test(command)
  );
}
```

### 4. URL Validation

Web operations are validated for safety:

```typescript
class URLValidator {
  static ALLOWED_PROTOCOLS = ['http', 'https'];

  static BLOCKED_DOMAINS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '169.254.169.254',  // AWS metadata
    'metadata.google.internal',  // GCP metadata
  ];

  static validate(url: string): ValidationResult {
    const parsed = new URL(url);

    // Protocol check
    if (!this.ALLOWED_PROTOCOLS.includes(parsed.protocol)) {
      return { valid: false, reason: 'Invalid protocol' };
    }

    // Domain check
    if (this.BLOCKED_DOMAINS.includes(parsed.hostname)) {
      return { valid: false, reason: 'Blocked domain' };
    }

    return { valid: true };
  }
}
```

### 5. Content Size Limits

Operations have size limits to prevent resource exhaustion:

| Operation | Default Limit | Configurable |
|-----------|--------------|--------------|
| File read | 10 MB | Yes |
| Web fetch | 10 MB | Yes |
| Shell output | 1 MB | Yes |
| Search results | 1000 | Yes |

### 6. Timeout System

Operations have configurable timeouts:

```typescript
const DEFAULT_TIMEOUTS = {
  file_read: 30000,      // 30 seconds
  file_write: 30000,
  shell_execute: 30000,  // Adjustable via settings
  web_fetch: 30000,
  grep: 60000,           // 60 seconds for large codebases
};
```

## Security Features Summary

| Feature | Protection Against | Implementation |
|---------|-------------------|----------------|
| Path traversal | Directory escape | Pattern matching + normalization |
| Command injection | Shell exploits | Whitelist + dangerous pattern block |
| Resource exhaustion | Memory/CPU abuse | Size limits + timeouts |
| SSRF attacks | Internal service access | Domain blacklist |
| Data exfiltration | Credential theft | Output filtering |

## Best Practices

1. **Always validate paths** before any file operation
2. **Use whitelists** instead of blacklists when possible
3. **Set appropriate timeouts** for long-running operations
4. **Implement logging** for security auditing
5. **Regular pattern updates** for emerging threats
