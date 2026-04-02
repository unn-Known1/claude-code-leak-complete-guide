# Memory System Architecture

## Overview

Claude Code implements a sophisticated memory management system with background consolidation, dynamic memory limits, and an intelligent autoDream process. This document details the memory architecture discovered in the leaked source code.

## Memory Management Components

### 1. MEMORY.md System

Claude Code maintains a project-specific memory file (`MEMORY.md`) for context persistence.

#### File Location

```
{project_root}/.claude/memory/MEMORY.md
```

#### Structure

```markdown
# Project Memory

## Last Updated
2026-04-01

## Project Context
[Summary of current project]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Important Patterns
[Reusable patterns discovered]

## TODO
- [Pending work]
```

### 2. autoDream - Background Memory Consolidation

The autoDream system runs as a forked subagent during idle periods.

#### Trigger System (Three-Gate)

Memory consolidation only occurs when ALL three gates pass:

| Gate | Condition | Purpose |
|------|-----------|---------|
| **Time Gate** | 24+ hours since last dream | Time-based trigger |
| **Session Gate** | 5+ sessions since last dream | Activity threshold |
| **Lock Gate** | Consolidation lock acquired | Prevents conflicts |

#### Consolidation Process

```
┌─────────────────────────────────────────────────────┐
│                   autoDream Process                  │
└─────────────────────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  ORIENT  │   │ GATHER   │   │CONSOLIDATE│
    │   Phase  │──▶│  Phase   │──▶│   Phase   │
    └──────────┘   └──────────┘   └──────────┘
                                         │
                                         ▼
                                   ┌──────────┐
                                   │  PRUNE   │
                                   │  Phase   │
                                   └──────────┘
```

##### Phase 1: Orient
- Initialize context from MEMORY.md
- Load recent conversation history
- Identify consolidation scope

##### Phase 2: Gather Recent Signal
- Collect observations from recent sessions
- Identify patterns and changes
- Note contradictions or updates needed

##### Phase 3: Consolidate
- Merge new observations with existing memory
- Remove contradictions
- Convert vague insights into concrete facts

##### Phase 4: Prune and Index
- Enforce memory limits (200 lines, ~25KB)
- Update search index
- Write final MEMORY.md

### 3. Memory Limits

| Limit | Value | Rationale |
|-------|-------|-----------|
| File lines | 200 | Readable summary |
| File size | ~25 KB | Efficient loading |
| Session buffer | 50 | Recent context |
| Consolidation interval | 24 hours | Balance freshness/efficiency |

### 4. Memory Operations

#### Reading Memory

```typescript
async function readMemory(projectPath: string): Promise<Memory> {
  const memoryPath = getMemoryPath(projectPath);

  if (!exists(memoryPath)) {
    return createEmptyMemory();
  }

  const content = await readFile(memoryPath);
  return parseMemory(content);
}
```

#### Writing Memory

```typescript
async function writeMemory(projectPath: string, memory: Memory): Promise<void> {
  const content = formatMemory(memory);

  // Enforce limits
  if (content.length > MAX_MEMORY_SIZE) {
    const pruned = pruneMemory(content, MAX_MEMORY_SIZE);
    await writeFile(getMemoryPath(projectPath), pruned);
  } else {
    await writeFile(getMemoryPath(projectPath), content);
  }
}
```

#### Consolidation Lock

```typescript
const LOCK_FILE = '.claude/memory/.dream-lock';

async function acquireConsolidationLock(): Promise<boolean> {
  try {
    await writeFile(LOCK_FILE, process.pid);
    return true;
  } catch {
    return false;  // Already locked
  }
}

async function releaseConsolidationLock(): Promise<void> {
  await rm(LOCK_FILE);
}
```

## Environment Variables

```bash
# Disable autoDream
CLAUDE_CODE_AUTO_DREAM=0

# Custom memory path
CLAUDE_CODE_MEMORY_PATH=/custom/path

# Force consolidation
CLAUDE_CODE_FORCE_DREAM=1

# Memory limits
CLAUDE_CODE_MEMORY_LINES=200
CLAUDE_CODE_MEMORY_KB=25
```

## Memory Triggers

### Automatic Triggers

1. **Session End**: Memory updated with session summary
2. **Idle Time**: autoDream triggers after 24+ hours
3. **Context Near Limit**: Aggressive pruning when approaching limits
4. **Project Switch**: Load new project memory

### Manual Triggers

```bash
# Force memory consolidation
claude dream

# Clear memory
claude memory clear

# Show memory contents
claude memory show
```

## Memory Format Specification

### Header Section

```markdown
# Memory Header
- Last Updated: {ISO timestamp}
- Consolidation Count: {number}
- Project Hash: {git commit or project identifier}
```

### Sections

| Section | Purpose | Auto-generated |
|---------|---------|-----------------|
| `## Last Updated` | Timestamp tracking | Yes |
| `## Project Context` | High-level understanding | autoDream |
| `## Key Decisions` | Important choices | Manual + autoDream |
| `## Important Patterns` | Reusable solutions | autoDream |
| `## TODO` | Pending work | Manual |

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Memory read time | ~10ms |
| Memory write time | ~50ms |
| Consolidation time | 30-120 seconds |
| Idle trigger delay | Up to 60 seconds |

## Edge Cases

### Lock Contention
If another process holds the lock, consolidation is skipped.

### Corruption Recovery
If MEMORY.md is corrupted, a fresh file is created with error note.

### Large Contexts
For very large projects, only recent/important entries are kept.

## Implementation Notes

The memory system is designed to be:

1. **Non-blocking**: Consolidation runs in background
2. **Idempotent**: Multiple consolidations produce same result
3. **Bounded**: Strict limits prevent runaway growth
4. **Recoverable**: Corruption doesn't lose all memory
