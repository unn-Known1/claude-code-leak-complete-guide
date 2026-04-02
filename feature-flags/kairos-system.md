# KAIROS - Always-On Autonomous Mode

## Overview

KAIROS is one of the most significant unreleased features discovered in Claude Code's source leak. It's an always-on autonomous daemon that monitors work and proactively takes actions without user prompting. Referenced over 150 times in the source code.

## System Design

### Core Concept

KAIROS transforms Claude Code from a reactive tool into a proactive assistant that:

1. **Watches**: Monitors your work in the background
2. **Logs**: Maintains append-only daily log files
3. **Acts**: Proactively executes within a budget
4. **Subscribes**: Listens to GitHub webhooks for events

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      KAIROS DAEMON                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   WATCHER   │  │   LOGGER   │  │  ACTUATOR   │          │
│  │  - Sessions │  │ - Daily    │  │ - 15s       │          │
│  │  - Files    │  │   Logs     │  │   Budget    │          │
│  │  - GitHub   │  │ - Append   │  │ - Proactive │          │
│  └─────────────┘  └─────────────┘  │   Actions   │          │
│                                     └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │   File   │    │  Shell   │    │  GitHub  │
        │ Observer │    │ Executor │    │  Webhook │
        └──────────┘    └──────────┘    └──────────┘
```

## Tick System

KAIROS operates on a "tick" cycle, receiving periodic prompts to decide whether to act.

### Tick Cycle

```typescript
interface KairosTick {
  timestamp: Date;
  sessionId: string;
  recentChanges: FileChange[];
  lastAction?: Action;
  budgetRemaining: number;
}

async function processTick(tick: KairosTick): Promise<Action | null> {
  // Check budget
  if (tick.budgetRemaining < MIN_BUDGET) {
    return null;  // No budget for action
  }

  // Analyze recent changes
  const signals = await gatherSignals(tick.recentChanges);

  // Decide action
  if (shouldProactivelyAct(signals)) {
    return executeProactiveAction(signals, tick);
  }

  return null;
}
```

### Budget System

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Total Budget | 15 seconds | Max blocking time per tick |
| Action Budget | 15 seconds | Single action limit |
| Tick Interval | Variable | Based on activity |

### Action Triggers

Actions are triggered by:

1. **File Changes**: New/modified files detected
2. **Git Events**: Commits, branches, PRs
3. **Error Patterns**: Compiler errors, test failures
4. **Time-based**: Scheduled checks

## Log System

### Daily Logs

KAIROS maintains append-only daily log files:

```
.claude/kairos/
├── 2026-03-31.log
├── 2026-04-01.log
└── 2026-04-02.log
```

### Log Format

```json
{
  "timestamp": "2026-04-02T14:30:00Z",
  "type": "observation",
  "session": "abc123",
  "data": {
    "action": "file_modified",
    "path": "src/main.ts",
    "detected_change": "new_import"
  }
}
```

```json
{
  "timestamp": "2026-04-02T14:30:05Z",
  "type": "action",
  "session": "abc123",
  "data": {
    "action": "suggest_import",
    "reason": "New import detected in file",
    "suggestion": "Add React import"
  }
}
```

## Proactive Actions

### Available Actions

| Action | Description | Budget Cost |
|--------|-------------|-------------|
| `SendUserFile` | Send file to user | 1s |
| `PushNotification` | Push notification | 0.5s |
| `SubscribePR` | Subscribe to PR events | 1s |
| `SuggestFix` | Suggest code fix | 2s |
| `RunTests` | Run relevant tests | 5s |

### Exclusive Tools

KAIROS has access to exclusive tools not available in normal mode:

```typescript
const KAIROS_EXCLUSIVE_TOOLS = [
  'SendUserFile',      // Send file notification
  'PushNotification',  // Push system notification
  'SubscribePR',       // GitHub PR subscription
];
```

## Configuration

### Environment Variables

```bash
# Enable KAIROS
CLAUDE_CODE_KAIROS=1

# Set budget per tick (seconds)
CLAUDE_CODE_KAIROS_BUDGET=15

# Set tick interval (seconds)
CLAUDE_CODE_KAIROS_INTERVAL=300

# Disable specific triggers
CLAUDE_CODE_KAIROS_TRIGGERS=file_change,github_event
```

### Feature Flag

KAIROS requires the `KAIROS` feature flag (compile-time) and `PROACTIVE` flag (runtime).

## Integration with Other Systems

### With autoDream

KAIROS observations feed into the autoDream system for memory consolidation:

```
KAIROS observes
       ↓
Log entry created
       ↓
autoDream reads logs
       ↓
Memory updated
```

### With GitHub

```typescript
// GitHub webhook subscriptions
const SUBSCRIPTIONS = {
  'issues.opened': true,
  'pull_request.opened': true,
  'pull_request.review_requested': true,
  'check_run.completed': true,
};
```

## Privacy Considerations

### What KAIROS Knows

- File changes in project
- Git operations
- Terminal output (filtered)
- GitHub events

### What KAIROS Doesn't Know

- Passwords/credentials
- Outside project files
- Browser history
- Private communications

### Data Retention

- Logs: 30 days rolling
- Observations: Session only
- Actions: Logged indefinitely

## Limitations

1. **15-second budget**: Cannot perform long operations
2. **Append-only logs**: Cannot modify past entries
3. **Single session**: Only monitors current project
4. **No persistence**: State lost on restart

## Security

### Access Control

KAIROS runs with the same permissions as the user.

### Audit Trail

All KAIROS actions are logged with:

- Timestamp
- Action taken
- Trigger
- Budget consumed

### Bypass Mode

In `bypass` permission mode, KAIROS can perform additional dangerous actions.

## Implementation Notes

The system demonstrates sophisticated autonomous agent design with:

1. **Budget Management**: Token bucket for resource control
2. **Event Sourcing**: Append-only logs for auditability
3. **Hierarchical Tools**: Exclusive tools with higher privileges
4. **Trigger System**: Configurable observation points
