# Feature Flag Reference

Complete catalog of 44 feature flags discovered in Claude Code's leaked source code, controlling over 20 unreleased capabilities.

## Flag Categories

### Core Systems

| Flag | Description | Dependencies |
|------|-------------|--------------|
| `KAIROS` | Always-on autonomous daemon | `PROACTIVE` |
| `BUDDY` | Tamagotchi companion system | - |
| `ULTRAPLAN` | Remote planning runtime | - |
| `UNDERCOVER` | Anti-leak mode for employees | - |
| `ANTI_DISTILLATION_CC` | Training data poisoning | - |
| `DREAM` | Memory consolidation | - |

### Agent Features

| Flag | Description | Dependencies |
|------|-------------|--------------|
| `AGENT` | Base agent system | - |
| `AGENT_TEAMS` | Multi-agent teams | `AGENT` |
| `AGENT_PROCESS` | Process-based agents | `AGENT` |
| `COORDINATOR` | Coordinator mode | `AGENT` |

### User Interface

| Flag | Description | Dependencies |
|------|-------------|--------------|
| `PENGUIN` | Penguin mode (fast) | - |
| `BRIDGE` | Bridge mode integration | - |
| `COMPUTER_USE` | Computer use system | - |

### Context & Memory

| Flag | Description | Dependencies |
|------|-------------|--------------|
| `CONTEXT_1M` | 1M token context | - |
| `MEMORY` | Basic memory system | - |
| `AUTO_DREAM` | autoDream consolidation | `MEMORY`, `DREAM` |
| `DREAM_LOCK` | Consolidation locking | `AUTO_DREAM` |

### Scheduling

| Flag | Description | Dependencies |
|------|-------------|--------------|
| `CRON` | Cron scheduling | - |
| `CRON_CREATE` | Create cron jobs | `CRON` |
| `CRON_DELETE` | Delete cron jobs | `CRON` |
| `SCHEDULE` | General scheduling | - |

### Git Operations

| Flag | Description | Dependencies |
|------|-------------|--------------|
| `GIT_WORKTREE` | Git worktree support | - |
| `GIT_STASH` | Git stash operations | - |

### Tools

| Flag | Description | Dependencies |
|------|-------------|--------------|
| `WEB_FETCH` | Web fetching | - |
| `WEB_SEARCH` | Web search | - |
| `WEB_BROWSER` | Browser automation | - |
| `TOOL_REGISTRY` | Plugin system | - |

### Beta Features

| Flag | Description | Status | Date |
|------|-------------|--------|------|
| `REDACT_THINKING` | Redacted reasoning | Beta | 2026-02-12 |
| `AFK_MODE` | Background work | Unreleased | 2026-01-31 |
| `ADVISOR_TOOL` | Advisor tool | Unreleased | 2026-03-01 |
| `CLI_INTERNAL` | Internal CLI features | Unreleased | 2026-02-09 |
| `TASK_BUDGETS` | Task budget management | Unreleased | 2026-03-13 |

## Complete Flag List

```typescript
// Core Flags
const FLAGS = {
  // Autonomous Systems
  KAIROS: false,                    // Always-on daemon
  BUDDY: false,                     // Pet system
  ULTRAPLAN: false,                 // Remote planning
  PROACTIVE: false,                 // Proactive mode

  // Agent Systems
  AGENT: false,                     // Base agent
  AGENT_TEAMS: false,               // Team support
  AGENT_PROCESS: false,             // Process agents
  COORDINATOR: false,               // Coordinator mode
  COORDINATOR_MODE: false,          // Coordinator env var

  // Memory
  MEMORY: false,                    // Memory system
  AUTO_DREAM: false,                // autoDream
  DREAM: false,                      // Dream system
  DREAM_LOCK: false,                 // Lock system

  // Anti-features
  UNDERCOVER: false,                // Undercover mode
  ANTI_DISTILLATION_CC: false,      // Anti-distillation

  // Context
  CONTEXT_1M: false,                 // 1M context

  // Interface
  PENGUIN: false,                   // Penguin mode
  BRIDGE: false,                     // Bridge mode
  COMPUTER_USE: false,              // Computer use

  // Scheduling
  CRON: false,                      // Cron support
  SCHEDULE: false,                   // Scheduling
  CRON_CREATE: false,               // Create jobs
  CRON_DELETE: false,                // Delete jobs

  // Git
  GIT_WORKTREE: false,              // Worktree
  GIT_STASH: false,                  // Stash ops

  // Web
  WEB_FETCH: false,                 // Fetch
  WEB_SEARCH: false,                 // Search
  WEB_BROWSER: false,               // Browser

  // Beta
  REDACT_THINKING: false,           // Redacted thinking
  AFK_MODE: false,                  // AFK mode
  ADVISOR_TOOL: false,              // Advisor
  CLI_INTERNAL: false,              // Internal CLI
  TASK_BUDGETS: false,              // Task budgets

  // Tools
  TOOL_REGISTRY: false,             // Plugin system
};
```

## Flag Dependencies

### Dependency Graph

```
AGENT
├── AGENT_TEAMS
│   └── AGENT_PROCESS
└── COORDINATOR
    └── COORDINATOR_MODE

MEMORY
├── AUTO_DREAM
│   ├── DREAM
│   └── DREAM_LOCK
└── ULTRAPLAN

KAIROS
└── PROACTIVE

CRON
├── CRON_CREATE
└── CRON_DELETE
```

## Environment Variable Mapping

Many flags have corresponding environment variables:

| Flag | Environment Variable | Default |
|------|---------------------|---------|
| `COORDINATOR_MODE` | `CLAUDE_CODE_COORDINATOR_MODE` | 0 |
| `UNDERCOVER` | `CLAUDE_CODE_UNDERCOVER` | auto |
| `PENGUIN` | `CLAUDE_CODE_PENGUIN_MODE` | 0 |
| `BUDDY` | `CLAUDE_CODE_BUDDY` | 0 |
| `KAIROS` | `CLAUDE_CODE_KAIROS` | 0 |

## Compile-Time vs Runtime

### Compile-Time Flags

These flags are baked into the binary:

```typescript
// Compile-time only
- BUDDY
- UNDERCOVER
- ANTI_DISTILLATION_CC
- COMPUTER_USE
```

### Runtime Flags

These can be toggled via environment:

```bash
# Runtime flags
CLAUDE_CODE_COORDINATOR_MODE=1
CLAUDE_CODE_KAIROS=1
CLAUDE_CODE_BUDDY=1
```

## Internal Codenames

The source revealed internal model codenames:

| Codename | Model Version | Status |
|----------|---------------|--------|
| `capybara` | Claude 4.6 | Production |
| `capybara-v2-fast` | Claude 4.6 fast | Production |
| `fennec` | Opus 4.6 | Internal |
| `numbat` | Unknown | Unreleased |
| `tengu` | Project codename | Internal |

## Flag Naming Convention

Flags follow patterns:

| Pattern | Example | Purpose |
|---------|---------|---------|
| `FEATURE_NAME` | `KAIROS` | Major features |
| `FEATURE_SUBFEATURE` | `CRON_CREATE` | Sub-features |
| `BEHAVIOR_MODE` | `UNDERCOVER` | Behavioral modes |

## Status Timeline

| Date | Features Released |
|------|------------------|
| 2025-08-07 | `CONTEXT_1M` added |
| 2026-01-31 | `AFK_MODE` added |
| 2026-02-09 | `CLI_INTERNAL` added |
| 2026-02-12 | `REDACT_THINKING` beta |
| 2026-03-01 | `ADVISOR_TOOL` added |
| 2026-03-13 | `TASK_BUDGETS` added |
| 2026-04-01 | `BUDDY` teaser launch |
| 2026-05-01 | `BUDDY` full launch (planned) |
