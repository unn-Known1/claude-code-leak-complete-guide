# MiniMax Agent Skill: Claude KAIROS

## Skill Metadata

**Skill Name**: `claude-kairos`
**Type**: Autonomous Agent Skill
**Category**: AI Agents / Claude Code
**Last Updated**: April 2026

---

## Skill Definition

```
Name: claude-kairos
Description: Expert skill on Anthropic's KAIROS - an always-on autonomous background agent that transforms Claude Code from reactive tool to persistent daemon with memory consolidation. Use when users ask about KAIROS, autonomous agents, Claude Code daemon mode, always-on AI, or proactive AI agents.
Trigger Keywords: KAIROS, autonomous agent, always-on AI, Claude Code daemon, background agent, proactive AI, autoDream
```

---

## Core Knowledge

### Overview

**KAIROS** is an unreleased always-on autonomous daemon mode hidden in Claude Code's source code (referenced over 150 times). It transforms Claude Code from a reactive request-response tool into a persistent, long-lived autonomous agent that operates continuously in the background.

### System Overview

| Aspect | Traditional Mode | KAIROS Mode |
|--------|-----------------|-------------|
| **Session Model** | Request-response | Long-lived background process |
| **Context** | Fresh each session | Progressive accumulation |
| **Initiation** | Human-initiated | Agent-initiated autonomous |
| **Monitoring** | Passive | Continuous active observation |
| **Action Model** | React to prompts | Proactive with autonomous decisions |

---

## Five Core Mechanisms

### 1. Proactive Tick Engine

The heartbeat that keeps the agent alive between conversational turns.

```javascript
// When message queue empties, inject <tick> instead of waiting
const tickContent = `<tick>${new Date().toLocaleTimeString()}</tick>`;
enqueue({ mode: 'prompt', value: tickContent, priority: 'later' });
void run();
```

**Key Characteristics**:
- Uses `setTimeout(0)` to yield to event loop first
- Makes proactive loop fully interruptible by user input
- Tick enters identical pipeline as user input

### 2. SleepTool (Throttle System)

Enables agent to yield control, preventing wasteful API calls.

```
Core Trade-offs:
- Each wake-up costs an API call
- Prompt cache expires after 5 minutes of inactivity
- Must balance responsiveness vs. cost
```

**Pacing Rules**:
- If no useful action on tick → MUST call Sleep
- Never respond with "still waiting" or "nothing to do"
- Return to sleep as quickly as possible

### 3. 15-Second Blocking Budget

Enforces strict 15-second limit on shell commands.

```javascript
const ASSISTANT_BLOCKING_BUDGET_MS = 15_000;
```

**Auto-Backgrounding**:
- Commands exceeding 15s automatically moved to background
- Agent notified when backgrounded
- Agent notified when command completes

### 4. Append-Only Memory System

Write-ahead log architecture for perpetual memory.

```
Path Pattern: logs/YYYY/MM/YYYY-MM-DD.md

Key Principle: Append-only - never rewrite logs
Distillation: Separate nightly process converts to structured memory
```

### 5. autoDream (Memory Consolidation)

Most sophisticated feature - background memory consolidation.

**Three Operations**:
1. **Merging Observations**: Combines info across sessions into unified representations
2. **Removing Contradictions**: Resolves conflicts by discarding outdated data
3. **Converting Vague to Facts**: Promotes tentative observations to firm assertions

**Activation Triggers**:
- Time Gate: 24+ hours since last dream
- Session Gate: 5+ sessions since last dream
- Activity Threshold: Extended user idle period

---

## Runtime Cycle

```
┌─────────────────────────────────────────────┐
│              KAIROS Runtime Cycle            │
└─────────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│   TICK   │  │   CHECK   │  │   LOG    │
│   Fires   │─▶│  for     │  │  Append  │
│          │  │  Work    │  │  Daily   │
└──────────┘  └──────────┘  └──────────┘
      │              │              │
      │              ▼              │
      │        ┌──────────┐        │
      │        │  Work    │        │
      │        │Available?│        │
      │        └────┬─────┘        │
      │         ┌───┴───┐          │
      │         ▼         ▼        │
      │    ┌─────────┐  ┌───────┐ │
      │    │ Execute │  │ Sleep │ │
      │    │  Work  │  │(Yield)│ │
      │    └───┬─────┘  └───────┘ │
      │        │                    │
      │        ▼                    │
      │  ┌─────────────┐           │
      │  │ 15s Budget │           │
      │  │   Check    │────────────┘
      │  └──────┬──────┘
      │         │ Auto-Background
      │         ▼
      │  ┌─────────────┐
      │  │Send Results │
      │  │(BriefTool) │
      │  └─────────────┘
      │         │
      └─────────┘
```

---

## Configuration

### Feature Flags

| Flag | Purpose | Default |
|------|---------|---------|
| `KAIROS` | Enable KAIROS daemon mode | `false` |
| `PROACTIVE` | Enable proactive tick engine | `false` |
| `AUTO_DREAM` | Enable memory consolidation | `false` |
| `DREAM` | Enable dream system | `false` |

### Environment Variables

```bash
# Enable KAIROS daemon
CLAUDE_CODE_KAIROS=1

# Set budget per tick (seconds)
CLAUDE_CODE_KAIROS_BUDGET=15

# Set tick interval (seconds)
CLAUDE_CODE_KAIROS_INTERVAL=300

# Disable autoDream
CLAUDE_CODE_AUTO_DREAM=0
```

---

## Exclusive Tools

KAIROS has access to tools not available in normal mode:

| Tool | Purpose | Budget Cost |
|------|---------|-------------|
| `SendUserMessage` | Route output to user | 0.5s |
| `PushNotification` | System notification | 0.5s |
| `SubscribePR` | GitHub webhook subscription | 1s |

---

## GitHub Integration

KAIROS can subscribe to GitHub events:

```typescript
const SUBSCRIPTIONS = {
  'issues.opened': true,
  'pull_request.opened': true,
  'pull_request.review_requested': true,
  'check_run.completed': true,
};
```

**Proactive Actions on Events**:
- PR opened → Review code, suggest improvements
- Issue opened → Analyze, suggest solution approach
- Review requested → Begin review process
- Check failed → Investigate, propose fix

---

## Memory System

### Memory Limits

| Parameter | Value |
|-----------|-------|
| MEMORY.md lines | 200 |
| MEMORY.md size | ~25KB |
| Topic file size | Variable |
| Log retention | 30 days rolling |

### Memory Flow

```
Observations → Daily Append Logs (RAW)
                      ↓
              autoDream Distillation
                      ↓
           MEMORY.md + Topic Files (Structured)
```

---

## Privacy Considerations

### What KAIROS Knows
- File changes in project directory
- Git operations and history
- Terminal output (filtered)
- GitHub events (if subscribed)
- Development patterns and habits

### What KAIROS Doesn't Access
- Passwords or credentials
- Files outside project directory
- Browser history
- Private communications

---

## Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| API Cost | Each wake-up costs API call | Sleep optimization |
| 15s Budget | Long commands backgrounded | Manual backgrounding |
| No Human Review | Actions taken without approval | Configurable approval modes |
| Context Drift | Memory may become stale | autoDream consolidation |
| False Memory | autoDream may create incorrect facts | User verification |

---

## Best Practices

### For Users
1. Start conservative with longer sleep intervals
2. Periodically review MEMORY.md for accuracy
3. Limit observation scope to relevant directories
4. Enable approval mode for destructive actions
5. Monitor API usage during initial deployment

### For Developers
1. Design for interruptibility
2. Checkpoint frequently for recovery
3. Expect long commands to move to background
4. Log meaningfully for future reference

---

## Quick Reference

```
System: KAIROS (Always-On Autonomous Agent)
Tick Engine: setTimeout(0) event loop injection
Sleep: Must sleep when idle, no idle narratives
Blocking Budget: 15 seconds auto-backgrounding
Memory: Append-only daily logs + autoDream distillation
Output: BriefTool with three-tier UI filtering
```

---

## Related Skills

- `claude-mythos-capybara` - Next-generation model powering advanced agents
- `claude-buddy` - Gamification companion system
- `claude-ultraplan` - Remote 30-minute planning
- `claude-undercover` - Anti-leak protection mode

---

## Source Information

**Based on**: Leaked Claude Code source (March 2026) - 512,000 lines across ~1,900 files

**Key Source Files**:
- `src/cli/print.ts` - Tick scheduling
- `src/tools/SleepTool/prompt.ts` - Sleep instructions
- `src/tools/BashTool/BashTool.tsx` - Blocking budget
- `src/memdir/memdir.ts` - Memory management

---

## Disclaimer

This skill document is compiled from leaked Claude Code source code. KAIROS is an unreleased feature with no confirmed public availability. Implementation details based on source code analysis and may not reflect final shipped functionality.
