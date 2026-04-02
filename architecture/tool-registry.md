# Tool Registry Architecture

## Overview

Claude Code implements a comprehensive tool registry system with over 40 distinct tools organized into functional categories. This document details the architecture discovered in the leaked source code.

## Tool Categories

### File Operations

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `FileReadTool` | Read file contents | LOW |
| `FileWriteTool` | Write files | MEDIUM |
| `FileEditTool` | Pattern-based editing | MEDIUM |
| `FileDeleteTool` | Remove files | HIGH |

### Shell Execution

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `BashTool` | Execute bash commands | HIGH |
| `PowerShellTool` | Execute PowerShell | HIGH |
| `REPLTool` | Interactive interpreter | MEDIUM |

### Search Operations

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `GlobTool` | Pattern-based file finding | LOW |
| `GrepTool` | Content search | LOW |

### Web Operations

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `WebFetchTool` | HTTP GET requests | MEDIUM |
| `WebSearchTool` | Search engine queries | LOW |
| `WebBrowserTool` | Browser automation | MEDIUM |

### Agent Operations

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `AgentTool` | Spawn sub-agents | HIGH |
| `SendMessageTool` | Inter-agent messaging | MEDIUM |
| `TeamCreateTool` | Create agent teams | HIGH |

### Task Management

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `TaskCreateTool` | Create task | LOW |
| `TaskGetTool` | Retrieve task | LOW |
| `TaskListTool` | List tasks | LOW |
| `TaskStopTool` | Cancel task | MEDIUM |

### Scheduling

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `ScheduleCronTool` | Cron scheduling | MEDIUM |
| `CronCreateTool` | Create cron job | MEDIUM |
| `CronDeleteTool` | Delete cron job | MEDIUM |

### Git Operations

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `EnterWorktreeTool` | Enter git worktree | MEDIUM |
| `ExitWorktreeTool` | Exit git worktree | LOW |

### Internal Tools

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `ConfigTool` | Configuration management | MEDIUM |
| `TungstenTool` | Internal operations | HIGH |
| `SuggestBackgroundPRTool` | PR suggestions | LOW |

## Architecture

### Registry Structure

```typescript
interface ToolRegistry {
  tools: Map<string, ToolDefinition>;
  categories: Map<string, ToolCategory>;
  permissions: Map<string, PermissionLevel>;
}

interface ToolDefinition {
  name: string;
  category: string;
  description: string;
  parameters: ParameterSchema;
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  requiresApproval: boolean;
  handler: ToolHandler;
}
```

### Tool Registration Flow

```
1. Application Startup
   ↓
2. Load tool definitions from registry
   ↓
3. Initialize tool handlers
   ↓
4. Register with permission system
   ↓
5. Tools available for agent use
```

## Plugin Architecture

### Loading Plugins

```typescript
// Plugin interface
interface ClaudeCodePlugin {
  name: string;
  version: string;
  tools: ToolDefinition[];
  onInit?: () => Promise<void>;
  onDestroy?: () => Promise<void>;
}

// Load custom plugins
CLAUDE_CODE_PLUGINS='./my-plugin.js'
```

### Built-in Plugin System

Claude Code supports third-party tools through a plugin interface:

```javascript
// Example plugin structure
{
  "name": "custom-tools",
  "tools": [
    {
      "name": "customDatabaseQuery",
      "handler": async (params) => { /* ... */ }
    }
  ]
}
```

## Query Engine

The source revealed a 46,000-line query engine responsible for:

1. **Tool Selection**: Choosing appropriate tools for tasks
2. **Parameter Validation**: Ensuring correct inputs
3. **Execution Ordering**: Managing tool call sequences
4. **Result Processing**: Transforming tool outputs

## Security Integration

### Permission Checking

```typescript
async function executeTool(toolName: string, params: any): Promise<Result> {
  // Check permission level
  const requiredLevel = registry.getPermissionLevel(toolName);
  const userLevel = getCurrentPermissionLevel();

  if (userLevel < requiredLevel) {
    throw new PermissionDeniedError(toolName);
  }

  // Check approval requirement
  if (tool.requiresApproval && !isApproved(toolName)) {
    return promptUser(toolName, params);
  }

  return tool.handler(params);
}
```

## Extending the Registry

### Adding Custom Tools

1. Create tool definition
2. Implement handler function
3. Register with permission system
4. Add to appropriate category

### Tool Development Guidelines

1. **Idempotency**: Same input should produce same output
2. **Error Handling**: Clear error messages with recovery suggestions
3. **Logging**: Structured logging for debugging
4. **Timeout**: Implement reasonable timeouts
5. **Validation**: Input validation before execution

## Configuration

### Environment Variables

```bash
# Enable specific tool categories
ENABLE_GIT_TOOLS=1
ENABLE_WEB_TOOLS=1
ENABLE_SCHEDULE_TOOLS=1

# Disable specific tools
DISABLE_TOOL=BashTool

# Custom tool paths
CLAUDE_CODE_TOOL_PATHS=/custom/tools
```

## Performance Considerations

1. **Lazy Loading**: Tools loaded on first use
2. **Caching**: Tool results cached where appropriate
3. **Batching**: Multiple operations batched when possible
4. **Streaming**: Long operations support streaming output
