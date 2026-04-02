# Multi-Agent Orchestration System

## Overview

Claude Code implements a sophisticated multi-agent system where a **Coordinator** orchestrates multiple **Worker** agents to handle complex tasks. This system was discovered in the leaked source code and represents a production-ready implementation of agent collaboration.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    COORDINATOR AGENT                        │
│  - Receives user task                                       │
│  - Decomposes into subtasks                                 │
│  - Assigns to workers                                        │
│  - Synthesizes final result                                 │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ WORKER 1 │    │ WORKER 2 │    │ WORKER 3 │
        │Research  │    │Research  │    │  Verify  │
        └──────────┘    └──────────┘    └──────────┘
```

### Four-Phase System

The coordinator follows a four-phase approach:

#### Phase 1: Research (Workers)
- Multiple worker agents independently research different aspects
- Workers communicate via `<task-notification>` XML messages
- Results are aggregated for synthesis

#### Phase 2: Synthesis (Coordinator)
- Coordinator analyzes worker findings
- Identifies patterns and conflicts
- Creates unified understanding

#### Phase 3: Implementation (Workers)
- Workers execute based on synthesized plan
- Parallel execution with coordination
- Real-time status updates

#### Phase 4: Verification (Workers)
- Independent verification agents check work
- Test execution
- Quality assurance

## Communication Protocol

### Task Notifications

Workers communicate using XML-based task notifications:

```xml
<task-notification type="status">
  <worker-id>worker-1</worker-id>
  <status>completed</status>
  <task-id>task-123</task-id>
  <result>
    <finding>Key discovery from worker 1</finding>
  </result>
</task-notification>
```

### Message Types

| Type | Purpose | Direction |
|------|---------|-----------|
| `task-assignment` | Assign task to worker | Coordinator → Worker |
| `status-update` | Report progress | Worker → Coordinator |
| `task-notification` | Share findings | Worker → Worker |
| `synthesis-request` | Request coordination | Worker → Coordinator |
| `verification-result` | Report verification | Worker → Coordinator |

## Environment Variables

```bash
# Enable coordinator mode
CLAUDE_CODE_COORDINATOR_MODE=1

# Configure worker count
CLAUDE_CODE_MAX_WORKERS=4

# Set timeout per phase
CLAUDE_CODE_PHASE_TIMEOUT=300
```

## Agent Teams & Swarm

Claude Code supports process-based teammates using tmux/iTerm2 panes:

```bash
# Enable team mode
CLAUDE_CODE_TEAM_MODE=1

# Team composition
CLAUDE_CODE_TEAM='researcher,coder,tester,reviewer'
```

## Process Architecture

### Spawning Workers

```python
# Pseudocode from leaked source
def spawn_worker(worker_type, task):
    worker_config = WORKER_CONFIGS[worker_type]
    process = tmux.new_window()
    process.execute(worker_config.binary, task)
    return WorkerHandle(process)
```

### Worker Types

| Type | Capabilities | Use Case |
|------|--------------|----------|
| `researcher` | Web search, file reading | Gathering information |
| `coder` | File write, shell commands | Implementation |
| `tester` | Execute tests, analyze output | Verification |
| `reviewer` | Code analysis, linting | Quality assurance |

## Limitations

1. **Context Window**: Shared context across all agents
2. **Token Budget**: Per-agent limits prevent runaway usage
3. **Race Conditions**: Concurrent writes require coordination
4. **Failure Handling**: Partial failures don't roll back completed work

## Best Practices

### When to Use Multi-Agent

- Complex tasks with independent subtasks
- Research requiring multiple sources
- Code requiring separate implementation and verification
- Large-scale refactoring

### When to Avoid

- Simple, linear tasks
- Tasks requiring sequential dependencies
- Limited token budget
- Single-file changes

## Implementation Notes

The multi-agent system fits within a single prompt rather than requiring a separate framework, demonstrating that sophisticated orchestration can be achieved through careful prompt engineering combined with structured tool use.
