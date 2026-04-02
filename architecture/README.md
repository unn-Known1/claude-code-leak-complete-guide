# Claude Code Architecture Deep-Dives

This directory contains detailed technical documentation of Claude Code's internal architecture, based on analysis of the leaked source code.

## Documentation Index

| Document | Description |
|----------|-------------|
| `multi-agent-system.md` | Four-phase coordinator/worker agent system |
| `tool-registry.md` | Plugin architecture with 40+ tools |
| `security-architecture.md` | Path traversal, risk classification, permissions |
| `memory-system.md` | autoDream, memory consolidation, MEMORY.md |
| `permission-system.md` | Four permission modes and bypass mechanisms |

## Overview

Claude Code's architecture is built around several core systems:

1. **Multi-Agent Orchestration**: A four-phase system (Research → Synthesis → Implementation → Verification)
2. **Tool Registry**: Modular plugin architecture with categorized tools
3. **Security Layer**: Path traversal protection and risk classification
4. **Memory System**: Background memory consolidation with three-gate triggers
5. **Permission System**: Four permission modes controlling operation restrictions

## Key Architectural Insights

### React Terminal Renderer

Claude Code uses a custom React + Ink terminal renderer with game-engine techniques, demonstrating that CLI tools can have modern UI patterns while maintaining text-based interaction.

### Modular System Prompts

The system prompt architecture uses `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` for cache-aware boundaries, allowing efficient prompt caching and modular instruction loading.

### Feature Flags

Over 44 feature flags gate 20+ unreleased capabilities, using compile-time feature flags with dead-code elimination for clean production builds.

## Usage

Each document can be read independently. For a comprehensive understanding, read in order:

1. Start with `tool-registry.md` to understand the tool system
2. Read `multi-agent-system.md` for orchestration patterns
3. Review `security-architecture.md` and `permission-system.md`
4. Finish with `memory-system.md` for persistence patterns
