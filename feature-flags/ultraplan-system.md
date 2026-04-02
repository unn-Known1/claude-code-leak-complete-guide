# ULTRAPLAN - Remote Planning System

## Overview

ULTRAPLAN is a sophisticated planning system that offloads complex planning tasks to a remote Cloud Container Runtime (CCR) session, utilizing Opus 4.6 with up to 30 minutes of dedicated think time.

## System Design

### Core Concept

For complex tasks that require extensive reasoning, ULTRAPLAN:

1. **Spawns Remote Session**: Creates CCR container
2. **Transfers Context**: Sends relevant project context
3. **Allocates Time**: Gives 30 minutes of compute
4. **Streams Results**: Browser UI to watch planning
5. **Teleports Output**: Special mechanism to return results

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      LOCAL CLI                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  CONTEXT    │  │  POLLING    │  │  TELEPORT   │          │
│  │  PACKAGER   │──▶│  AGENT      │◀──│  RECEIVER   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│         │              │                   │                 │
└─────────│──────────────│───────────────────│─────────────────┘
          │              │                   │
          ▼              │                   │
┌─────────────────────────────────────────────────────────────┐
│                    REMOTE CCR                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  OPUS 4.6   │  │  THINKING   │  │  OUTPUT     │          │
│  │  MODEL      │──▶│  (30 min)   │──▶│  GENERATOR  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Planning Flow

### Step 1: Context Packaging

```typescript
async function packageContext(task: Task): Promise<PlanningContext> {
  return {
    projectFiles: await gatherRelevantFiles(task),
    recentHistory: await getConversationHistory(),
    constraints: extractConstraints(task),
    objectives: extractObjectives(task),
    timeline: task.deadline,
  };
}
```

### Step 2: Remote Session Creation

```typescript
async function createPlanningSession(
  context: PlanningContext
): Promise<SessionHandle> {
  // Request CCR with Opus 4.6
  const session = await CCR.create({
    model: 'opus-4.6',
    computeBudget: '30min',
    memory: '64gb',
  });

  // Send context
  await session.sendContext(context);

  return session;
}
```

### Step 3: Planning Execution

The remote session runs with:

| Resource | Allocation |
|----------|------------|
| Model | Opus 4.6 |
| Time | 30 minutes |
| Memory | 64 GB |
| Context | Full project |

### Step 4: Progress Polling

```typescript
async function pollForResults(
  session: SessionHandle,
  onProgress: (progress: Progress) => void
): Promise<Plan> {
  while (!session.isComplete()) {
    const progress = await session.getProgress();
    onProgress(progress);

    // Poll every 3 seconds
    await sleep(3000);
  }

  return session.getResults();
}
```

### Step 5: Result Teleportation

Results are returned via a special sentinel value:

```typescript
// The plan is injected back using a special mechanism
const TELEPORT_TOKEN = '__ULTRAPLAN_TELEPORT_LOCAL__';

async function receivePlan(session: SessionHandle): Promise<Plan> {
  const rawResults = await session.getResults();

  // Find and process teleport tokens
  if (rawResults.includes(TELEPORT_TOKEN)) {
    const plan = extractPlanFromToken(rawResults);
    return plan;
  }

  return parseResults(rawResults);
}
```

## Browser UI

### Purpose

A web-based interface allows users to:

1. **Watch Progress**: Real-time streaming of planning
2. **Approve/Reject**: Accept or discard generated plans
3. **Iterate**: Request modifications
4. **Cancel**: Abort long-running plans

### Interface

```
┌─────────────────────────────────────────────────────────────┐
│ ULTRAPLAN - Remote Planning Session                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Status: Planning... (12:34 remaining)                      │
│  Phase: Analyzing dependencies                             │
│                                                             │
│  Progress: ████████████░░░░░░░░░░░░░ 45%                   │
│                                                             │
│  Current Thought:                                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ I've analyzed the codebase and identified 3 main       ││
│  │ architectural patterns that need refactoring...        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  [View Full Plan]  [Approve]  [Request Changes]  [Cancel]  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### URL Format

```
http://localhost:8976/plan/{session_id}
```

## Use Cases

### Complex Refactoring

When facing a large-scale refactor:

```
User: "Help me refactor our monolith into microservices"
Claude: "This is a complex task. Let me use ULTRAPLAN to create a detailed migration plan."
```

### Architecture Decisions

For significant architectural choices:

```
User: "Should we switch from REST to GraphQL?"
Claude: "This deserves careful consideration. ULTRAPLAN can analyze both approaches with your specific constraints."
```

### Multi-Phase Projects

For projects with many interdependent phases:

```
User: "Plan out the next 6 months of development"
Claude: "That's a significant planning task. Let me use ULTRAPLAN to create a comprehensive roadmap."
```

## Feature Flag

```typescript
const ULTRAPLAN = true;  // Compile-time flag
```

### Environment Variables

```bash
# Enable ULTRAPLAN
CLAUDE_CODE_ULTRAPLAN=1

# Set timeout
CLAUDE_CODE_ULTRAPLAN_TIMEOUT=1800  # 30 minutes

# Set container region
CLAUDE_CODE_CCR_REGION=us-east-1
```

## CCR (Cloud Container Runtime)

### Container Spec

```yaml
spec:
  name: ultraplan-{session_id}
  image: anthropic/plan-engine:latest
  resources:
    cpu: 8
    memory: 64GB
    gpu: 1xA100
  timeout: 1800s  # 30 minutes
  model: opus-4.6
```

### Cost Implications

| Resource | Cost per 30 min |
|----------|-----------------|
| Compute | ~$0.50 |
| Model API | ~$5.00 |
| **Total** | ~$5.50 |

### Cost Control

```typescript
// Warn user before starting
async function confirmPlanningCost(): Promise<boolean> {
  const estimated = calculateCost({
    duration: '30min',
    model: 'opus-4.6',
  });

  return prompt(
    `This will cost approximately $${estimated.toFixed(2)}. Continue?`
  );
}
```

## Limitations

1. **Cost**: ~$5.50 per planning session
2. **Time**: Results take up to 30 minutes
3. **Connectivity**: Requires CCR access
4. **Context Size**: Large contexts may be truncated
5. **No Edit During**: Cannot modify plan while generating

## Integration with KAIROS

ULTRAPLAN can be triggered by KAIROS for proactive planning:

```typescript
// KAIROS detected complex task
if (detectComplexity(task) > THRESHOLD) {
  await suggestToUser(
    "This looks like a complex task. Should I use ULTRAPLAN for detailed planning?"
  );
}
```

## Privacy

### Data Handling

- Project files sent to CCR
- Encrypted in transit
- Not used for training
- Deleted after session

### Sensitive Data

Users are warned before sending:

```
⚠️ Warning: This will send the following files to Anthropic's cloud:

  - src/auth/*.ts (15 files)
  - src/config.yaml

  Sensitive patterns detected: API keys will be redacted.

  [Continue] [Review Files] [Cancel]
```

## Future Enhancements

The source code suggests future features:

- **Team Planning**: Multiple CCR sessions for parallel analysis
- **Incremental Planning**: Update existing plans
- **Cost Sharing**: Split costs across team
- **Custom Models**: Use fine-tuned planning models

## Comparison with Local Planning

| Aspect | Local | ULTRAPLAN |
|--------|-------|----------|
| Time | Seconds | 30 minutes |
| Context | Limited | Full project |
| Quality | Good | Thorough |
| Cost | Free | ~$5.50 |
| Availability | Always | Requires CCR |

## Implementation Notes

ULTRAPLAN demonstrates:

1. **Resource Management**: Token bucket for expensive operations
2. **Streaming UI**: Real-time progress updates
3. **Context Transfer**: Efficient serialization
4. **Error Recovery**: Session cleanup on failure
