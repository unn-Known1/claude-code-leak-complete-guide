# Claude KAIROS - Always-On Autonomous Agent Skill

## Skill Overview

**System Name**: KAIROS
**Type**: Always-On Autonomous Background Agent
**Reference Count**: Over 150 references in Claude Code source
**Status**: Unreleased Feature Flag
**Integration**: Claude Code daemon mode

KAIROS transforms Claude Code from a reactive request-response tool into a persistent, long-lived autonomous agent that operates continuously in the background, accumulating understanding and taking proactive actions on behalf of the user.

---

## Executive Summary

KAIROS represents a fundamental paradigm shift in AI coding assistants. Unlike traditional AI tools that respond only when prompted, KAIROS introduces an always-on daemon mode that continuously monitors development activity, learns from observations, and autonomously takes actions when opportunities or issues are detected. The system maintains persistent context across sessions, enabling it to build progressively richer understanding of projects, patterns, and user preferences.

The architecture consists of five independent but interconnected mechanisms: the proactive tick engine, sleep/throttle system, append-only memory architecture, blocking budget enforcement, and dedicated messaging layer. Together, these create an autonomous agent capable of sustained operation without human intervention.

---

## Core Architecture

### System Overview

KAIROS operates as a daemon that persists beyond individual conversation sessions. When activated, it fundamentally changes how Claude Code behaves:

| Aspect | Traditional Mode | KAIROS Mode |
|--------|-----------------|-------------|
| **Session Model** | Request-response | Long-lived background process |
| **Context** | Fresh each session | Progressive accumulation |
| **Initiation** | Human-initiated | Agent-initiated autonomous |
| **Monitoring** | Passive | Continuous active observation |
| **Action Model** | React to prompts | Proactive with autonomous decisions |

### Five Core Mechanisms

| Mechanism | Purpose | Technical Implementation |
|-----------|---------|----------------------|
| **Tick Loop** | Proactive engine keeping agent alive | `setTimeout(0)` event loop injection |
| **SleepTool** | Throttles ticks to prevent wasted API calls | Explicit yield control |
| **Blocking Budget (15s)** | Auto-backgrounds long commands | `ASSISTANT_BLOCKING_BUDGET_MS = 15000` |
| **Append-Only Daily Logs** | Write-ahead log for perpetual memory | `logs/YYYY/MM/YYYY-MM-DD.md` |
| **SendUserMessage** | Dedicated output channel | BriefTool for user-facing results |

---

## Mechanism 1: Proactive Tick Engine

### Overview

The tick loop is the heartbeat of KAIROS, keeping the agent alive between conversational turns. When the message queue empties in normal mode, Claude Code waits for user input. In KAIROS mode, the system injects a `<tick>` message instead of waiting.

### Technical Implementation

```javascript
const scheduleProactiveTick =
  feature('PROACTIVE') || feature('KAIROS')
    ? () => {
        setTimeout(() => {
          if (
            !proactiveModule?.isProactiveActive() ||
            proactiveModule.isProactivePaused() ||
            inputClosed
          ) {
            return
          }
          const tickContent = `<${TICK_TAG}>${new Date().toLocaleTimeString()}</${TICK_TAG}>`
          enqueue({
            mode: 'prompt' as const,
            value: tickContent,
            uuid: randomUUID(),
            priority: 'later',
            isMeta: true,
          })
          void run()
        }, 0)
      }
    : undefined
```

### Key Characteristics

1. **Event Loop Yielding**: `setTimeout(0)` yields to the event loop first, allowing pending stdin messages to process before the tick fires. This makes the proactive loop fully interruptible.

2. **User Input Preemption**: If user input arrives while a tick is scheduled, the input takes precedence and the tick waits.

3. **Same Pipeline**: The tick enters the identical message processing pipeline as user input, ensuring consistent behavior regardless of message origin.

4. **Priority System**: Tick messages use `priority: 'later'` to ensure they don't preempt higher-priority messages.

### Tick Content Format

```xml
<tick>14:30:05</tick>
```

The tick contains the current local time, allowing the agent to make time-aware decisions.

### System Prompt Instructions for Tick

```
You are running autonomously. You will receive `<tick>` prompts that keep you
alive between turns — just treat them as "you're awake, what now?" The time
in each `<tick>` is the user's current local time. Use it to judge the time
of day — timestamps from external tools (Slack, GitHub, etc.) may be in a
different timezone.

Multiple ticks may be batched into a single message. This is normal — just
process the latest one. Never echo or repeat tick content in your response.
```

---

## Mechanism 2: SleepTool (Throttle System)

### Overview

SleepTool enables the agent to explicitly yield control, preventing wasteful API calls during idle periods. This is the primary cost-control mechanism, allowing KAIROS to remain responsive without incurring charges for unnecessary wake-ups.

### SleepTool Prompt

```
Wait for a specified duration.
The user can interrupt the sleep at any time.

Use this when the user tells you to sleep or rest, when you
have nothing to do, or when you're waiting for something.

You may receive <tick> prompts — these are periodic check-ins.
Look for useful work to do before sleeping.

You can call this concurrently with other tools — it won't
interfere with them.

Prefer this over `Bash(sleep ...)` — it doesn't hold a shell
process.

Each wake-up costs an API call, but the prompt cache expires
after 5 minutes of inactivity — balance accordingly.
```

### Core Trade-offs

| Factor | Consideration |
|--------|---------------|
| **API Cost** | Each wake-up incurs an API call |
| **Cache Expiration** | Prompt cache expires after 5 minutes of inactivity |
| **Responsiveness** | Longer sleeps reduce responsiveness |
| **Efficiency** | Shorter sleeps increase cost |

### Pacing Rules (System Prompt)

```
Use the Sleep tool to control how long you wait between actions. Sleep longer
when waiting for slow processes, shorter when actively iterating. Each wake-up
costs an API call, but the prompt cache expires after 5 minutes of inactivity
— balance accordingly.

If you have nothing useful to do on a tick, you MUST call Sleep. Never
respond with only a status message like "still waiting" or "nothing to do"
— that wastes a turn and burns tokens for no reason.
```

### Idle Behavior Rules

The agent is instructed:

1. **Must Sleep When Idle**: If no useful action exists, Sleep MUST be called
2. **No Idle Narratives**: Never output text describing idle state
3. **Immediate Yield**: Return to sleep as quickly as possible when done
4. **Continuous Checking**: Each wake-up is an opportunity to find work

---

## Mechanism 3: 15-Second Blocking Budget

### Overview

KAIROS enforces a strict 15-second blocking budget on shell commands. Any command exceeding this duration is automatically backgrounded, ensuring the agent remains responsive to new ticks and user input.

### Configuration

```javascript
const ASSISTANT_BLOCKING_BUDGET_MS = 15_000;
```

### Auto-Backgrounding Implementation

```javascript
if (feature('KAIROS') && getKairosActive() && isMainThread
    && !isBackgroundTasksDisabled && run_in_background !== true) {
  setTimeout(() => {
    if (shellCommand.status === 'running'
        && backgroundShellId === undefined) {
      assistantAutoBackgrounded = true;
      startBackgrounding(/* ... */);
    }
  }, ASSISTANT_BLOCKING_BUDGET_MS).unref();
}
```

### Agent Notification

When a command is auto-backgrounded, the agent receives:

```
Command exceeded the assistant-mode blocking budget
(15s) and was moved to the background with ID: {backgroundTaskId}.
It is still running — you will be notified when it completes.
Output is being written to: {outputPath}.
In assistant mode, delegate long-running work
to a subagent or use run_in_background to keep this conversation
responsive.
```

### Background Task Management

| Aspect | Behavior |
|--------|----------|
| **Notification** | Agent alerted when backgrounded |
| **Completion** | Agent notified when command completes |
| **Output** | Written to specified path |
| **Intervention** | Agent can check, cancel, or modify |

---

## Mechanism 4: Append-Only Memory System

### Overview

Unlike traditional memory that overwrites previous entries, KAIROS uses a write-ahead log architecture. Observations are appended to daily log files, with a separate distillation process converting raw logs into structured memory.

### Daily Log Structure

**Path Pattern**: `logs/YYYY/MM/YYYY-MM-DD.md`

```
logs/
├── 2026/
│   ├── 03/
│   │   ├── 2026-03-30.md
│   │   └── 2026-03-31.md
│   └── 04/
│       └── 2026-04-01.md
```

### Daily Log Prompt

```
This session is long-lived. As you work, record anything worth
remembering by **appending** to today's daily log file:

`${logPathPattern}`

Do not rewrite or reorganize the log — it is append-only.
A separate nightly process distills these logs into
`MEMORY.md` and topic files.
```

### Memory Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Observations  │───▶│ Daily Append    │───▶│  autoDream     │
│   (During Work) │    │ Logs (RAW)     │    │  Distillation  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │  MEMORY.md      │
                                              │  Topic Files    │
                                              │  (Structured)   │
                                              └─────────────────┘
```

### Key Principles

1. **Append Only**: Never rewrite or reorganize logs
2. **Incremental Recording**: Add observations as they occur
3. **Date-Based Organization**: Automatic file rotation
4. **Nightly Distillation**: Separate process converts to structured memory

---

## Mechanism 5: autoDream (Memory Consolidation)

### Overview

autoDream is KAIROS's most sophisticated feature—a background memory consolidation system that runs during user idle periods. It transforms raw daily observations into structured, queryable knowledge.

### Activation Triggers

autoDream activates during user inactivity periods. The system monitors for:

| Trigger | Condition |
|---------|-----------|
| **Time Gate** | 24+ hours since last dream |
| **Session Gate** | 5+ sessions since last dream |
| **Activity Threshold** | User has been idle for extended period |

### Three Consolidation Operations

#### 1. Merging Observations

Combines information gathered across different sessions, files, and interactions into unified representations:

```markdown
# Before Consolidation
Session 1: "Function X might handle authentication"
Session 2: "Function X calls auth_service.validate()"
Session 3: "Function X is called from login_flow"

# After autoDream
Fact: Function X handles authentication via auth_service.validate()
```

#### 2. Removing Logical Contradictions

Resolves conflicting information by discarding outdated data:

```markdown
# Before
Earlier: "API endpoint returns JSON"
Later observation: "API endpoint actually returns XML"

# After autoDream
Correction: API endpoint returns XML (earlier observation was incorrect)
```

#### 3. Converting Vague Insights to Facts

Promotes tentative observations to firm assertions based on accumulated evidence:

```markdown
# Before
"This function might handle authentication"
"Maybe related to user login"
"Possibly security-critical"

# After autoDream
Confirmed: This function handles user authentication for the login flow.
It validates credentials and creates session tokens.
```

### autoDream Execution

The distillation process:

1. **Reads** all daily logs since last distillation
2. **Identifies** patterns and recurring themes
3. **Resolves** contradictions and outdated information
4. **Generates** structured topic files
5. **Updates** MEMORY.md index
6. **Prunes** logs beyond retention period

### Memory Limits

| Parameter | Value | Enforcement |
|-----------|-------|--------------|
| **MEMORY.md lines** | 200 | Hard limit |
| **MEMORY.md size** | ~25KB | Approximate |
| **Topic file size** | Variable | Context-dependent |
| **Log retention** | 30 days | Rolling window |

---

## Messaging Layer: SendUserMessage

### Overview

SendUserMessage (implemented as BriefTool internally) handles output routing in background mode, ensuring appropriate information delivery based on context.

### Prompt Contract

```
SendUserMessage is where your replies go. Text outside it is visible
if the user expands the detail view, but most won't — assume unread.

The failure mode: the real answer lives in plain text while
SendUserMessage just says "done!" — they see "done!" and miss
everything.
```

### Status Field Usage

| Status | Usage | Context |
|--------|-------|---------|
| `'normal'` | Replies to user messages | Interactive sessions |
| `'proactive'` | Unsolicited updates | KAIROS background actions |

### Three-Tier UI Filtering

```javascript
// Tier 1: Brief-only mode
// SendUserMessage + user input only

// Tier 2: Default mode (drop redundant text)
// When SendUserMessage was called, drop assistant filler text

// Tier 3: Transcript mode (ctrl+o)
// Truly unfiltered transcript view
```

### Long Work Pattern

For extended operations, KAIROS uses an acknowledgment → work → result pattern:

```
1. Acknowledge: "Starting analysis..."
2. Work: [Perform analysis]
3. Checkpoint: [Optional] "Found issue X"
4. Result: Final output
```

Checkpoints are sent when:
- A significant decision is made
- A surprise or obstacle is encountered
- A phase boundary is crossed
- Work is complete

---

## Runtime Cycle

### Complete KAIROS Operation Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                        KAIROS Runtime Cycle                      │
└─────────────────────────────────────────────────────────────────┘
                              │
      ┌───────────────────────┼───────────────────────┐
      ▼                       ▼                       ▼
┌──────────┐           ┌──────────┐           ┌──────────┐
│   TICK   │           │   CHECK   │           │   LOG    │
│   Fires   │──────────▶│  for     │           │  Append  │
│          │           │  Work    │           │  Daily   │
└──────────┘           └──────────┘           └──────────┘
      │                       │                       │
      │                       ▼                       │
      │               ┌──────────────┐               │
      │               │  Work       │               │
      │               │  Available? │               │
      │               └──────────────┘               │
      │                  │     │                     │
      │         ┌────────┘     └────────┐            │
      │         ▼                          ▼           │
      │   ┌──────────┐              ┌──────────┐     │
      │   │ Execute  │              │  Sleep   │     │
      │   │  Work   │              │ (Yield)  │     │
      │   └────┬────┘              └──────────┘     │
      │        │                                          │
      │        ▼                                          │
      │   ┌──────────────┐                               │
      │   │ 15s Budget   │                               │
      │   │ Check        │                               │
      │   └──────┬───────┘                               │
      │          │ Auto-Background                        │
      │          ▼ if exceeded                           │
      │   ┌──────────────┐                               │
      │   │Send Results  │◀──────────────────────────────┘
      │   │(BriefTool)   │
      │   └──────┬───────┘
      │          │
      │          ▼
      │   ┌──────────────┐
      │   │ Queue Empties│
      │   └──────┬───────┘
      │          │
      │          ▼
      │   Schedule Next Tick
      │          │
      └──────────┘
```

### Step-by-Step Flow

1. **Tick fires** → System injects `<tick>` message into queue
2. **Agent awakens** → Receives tick with current time
3. **Checks for work** → Examines conversation history, pending commands, unresolved threads
4. **Executes commands** → Runs necessary operations (blocking budget enforced)
5. **Auto-backgrounds** → Long commands moved to background after 15 seconds
6. **Logs observations** → Appends to daily log file
7. **Sends results** → Through SendUserMessage with appropriate status
8. **Queue empties** → Tick scheduling mechanism activated
9. **Agent decides** → Sleep if no work, otherwise continues
10. **Cycle repeats** → Continues until deactivated or interrupted

---

## Configuration and Environment Variables

### Feature Flags

| Flag | Purpose | Default |
|------|---------|---------|
| `KAIROS` | Enable KAIROS daemon mode | `false` |
| `PROACTIVE` | Enable proactive tick engine | `false` |
| `AUTO_DREAM` | Enable memory consolidation | `false` |
| `DREAM` | Enable dream system | `false` |
| `DREAM_LOCK` | Enable consolidation locking | `false` |

### Environment Variables

```bash
# Enable KAIROS daemon
CLAUDE_CODE_KAIROS=1

# Set budget per tick (seconds)
CLAUDE_CODE_KAIROS_BUDGET=15

# Set tick interval (seconds)
CLAUDE_CODE_KAIROS_INTERVAL=300

# Disable specific triggers
CLAUDE_CODE_KAIROS_TRIGGERS=file_change,github_event

# Disable autoDream
CLAUDE_CODE_AUTO_DREAM=0

# Custom memory path
CLAUDE_CODE_MEMORY_PATH=/custom/path
```

### Exclusive Tools

KAIROS has access to exclusive tools not available in normal mode:

| Tool | Purpose | Budget Cost |
|------|---------|-------------|
| `SendUserMessage` | Route output to user | 0.5s |
| `PushNotification` | System notification | 0.5s |
| `SubscribePR` | GitHub webhook subscription | 1s |

---

## GitHub Integration

### Webhook Subscriptions

KAIROS can subscribe to GitHub events:

```typescript
const SUBSCRIPTIONS = {
  'issues.opened': true,
  'pull_request.opened': true,
  'pull_request.review_requested': true,
  'check_run.completed': true,
  'commit.push': false,
  'release.published': false,
};
```

### Proactive Actions on Events

| Event | Action |
|-------|--------|
| PR opened | Review code, suggest improvements |
| Issue opened | Analyze, suggest solution approach |
| Review requested | Begin review process |
| Check failed | Investigate, propose fix |

---

## Privacy and Security Considerations

### What KAIROS Knows

- File changes in project directory
- Git operations and history
- Terminal output (filtered for sensitive data)
- GitHub events (if subscribed)
- Development patterns and habits
- Code structure and architecture

### What KAIROS Doesn't Access

- Passwords or credentials
- Files outside project directory
- Browser history
- Private communications
- System-level information beyond project

### Data Retention

| Data Type | Retention | Location |
|-----------|-----------|----------|
| Daily logs | 30 days rolling | Local project |
| Consolidated memory | Indefinite | MEMORY.md |
| Topic files | Indefinite | Local project |
| Background command output | Until consumed | Temporary files |

### Privacy Controls

- All data stored locally by default
- No automatic server transmission
- User-configurable observation scope
- Manual memory review capability
- Session pause/stop controls

---

## Limitations and Known Issues

### Current Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **API Cost** | Each wake-up costs API call | Sleep optimization |
| **15s Budget** | Long commands backgrounded | Manual backgrounding |
| **No Human Review** | Actions taken without approval | Configurable approval modes |
| **Context Drift** | Memory may become stale | autoDream consolidation |
| **False Memory** | autoDream may create incorrect facts | User verification |

### Edge Cases

1. **Lock Contention**: If another process holds consolidation lock, autoDream skipped
2. **Log Corruption**: Fresh file created if MEMORY.md corrupted
3. **Large Contexts**: Only recent/important entries retained for very large projects
4. **Timezone Confusion**: External tool timestamps may differ from local time

### Performance Characteristics

| Metric | Value |
|--------|-------|
| Tick processing time | ~100-500ms |
| Sleep minimum | 1 second |
| Memory read | ~10ms |
| Memory write | ~50ms |
| autoDream duration | 30-120 seconds |
| Idle tick interval | Variable (user configurable) |

---

## Best Practices

### For Users

1. **Start Conservative**: Begin with longer sleep intervals
2. **Review Memory**: Periodically check MEMORY.md for accuracy
3. **Configure Scope**: Limit observation to relevant directories
4. **Use Approval Mode**: Enable approval for destructive actions
5. **Monitor Costs**: Track API usage during initial deployment

### For Developers

1. **Design for Interruptibility**: Assume actions may be preempted
2. **Checkpoint Frequently**: Save progress for recovery
3. **Handle Backgrounding**: Expect long commands to move to background
4. **Log Meaningfully**: Record observations for future reference
5. **Respect Resource Limits**: Stay within memory constraints

### Configuration Recommendations

```yaml
# Initial deployment
kairos:
  tick_interval: 300  # 5 minutes
  sleep_threshold: 60  # seconds
  auto_dream: true
  
# Active development
kairos:
  tick_interval: 60  # 1 minute
  sleep_threshold: 30
  auto_dream: true
  
# Monitoring mode
kairos:
  tick_interval: 600  # 10 minutes
  sleep_threshold: 300
  auto_dream: false
```

---

## Comparison with Traditional AI Assistants

| Aspect | Traditional Assistant | KAIROS Agent |
|--------|---------------------|--------------|
| **Availability** | On-demand | Always-on |
| **Proactivity** | Reactive only | Proactive discovery |
| **Memory** | Session-only | Perpetual |
| **Actions** | User-requested | Autonomous |
| **Learning** | None | Continuous |
| **Context** | Fresh each time | Accumulated |
| **Cost** | Per-request | Continuous |
| **Interruptibility** | Full | Partial |

---

## Future Enhancements

Based on source code analysis, potential future features include:

| Feature | Status | Notes |
|---------|--------|-------|
| **Multi-project awareness** | Speculated | Cross-project context |
| **Team collaboration** | Speculated | Shared memory spaces |
| **Custom memory stores** | Possible | External knowledge bases |
| **Scheduled dreaming** | Possible | Time-based consolidation |
| **Selective forgetting** | Possible | Privacy controls |

---

## Reference Implementation

### Source Files

From the Claude Code leak:

- `src/cli/print.ts` - Tick scheduling
- `src/constants/prompts.ts` - System prompt templates
- `src/tools/SleepTool/prompt.ts` - Sleep instruction prompt
- `src/tools/BashTool/BashTool.tsx` - Blocking budget enforcement
- `src/memdir/memdir.ts` - Memory management
- `src/tools/BriefTool/prompt.ts` - Messaging layer
- `src/components/Messages.tsx` - UI filtering logic

### Key Constants

```typescript
const ASSISTANT_BLOCKING_BUDGET_MS = 15_000;
const PROMPT_CACHE_EXPIRY_MS = 5 * 60 * 1000;  // 5 minutes
const MEMORY_MAX_LINES = 200;
const MEMORY_MAX_SIZE_APPROX = 25 * 1024;  // ~25KB
```

---

## Skill Maintenance

**Last Updated**: April 2026
**Source Reliability**: Based on leaked Claude Code source (March 2026)
**Verification Status**: Technical implementation details verified from source
**Maintainer**: Claude Code Analysis Community

---

## Disclaimer

This skill document is compiled from leaked Claude Code source code and analysis. KAIROS is an unreleased feature with no confirmed public availability timeline. The implementation details are based on source code analysis and may not reflect final shipped functionality. All information should be verified against official Anthropic communications.
