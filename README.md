# Claude Code Source Code Leak - Complete Guide & Documentation

<p align="center">
  <img src="assets/banner.svg" alt="Claude Code Leak Banner" width="100%"/>
</p>

<div align="center">

![Leak Status](https://img.shields.io/badge/Leak%20Status-Confirmed-brightgreen)
![Date](https://img.shields.io/badge/Date-March%2031%2C%202026-orange)
![Source Map Size](https://img.shields.io/badge/Source%20Map%20Size-59.8%20MB-blue)
![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-512%2C000+-red)
![Files](https://img.shields.io/badge/Files-248-green)
![Platform](https://img.shields.io/badge/Platform-npm%20Registry-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## Table of Contents

- [What Happened?](#what-happened)
- [The Technical Details](#the-technical-details)
- [Repository Contents](#repository-contents)
- [Leaked Source Code](#leaked-source-code)
- [Clean Room Rust Implementation](#clean-room-rust-implementation)
- [Key Discoveries](#key-discoveries)
- [Timeline of Events](#timeline-of-events)
- [Security Implications](#security-implications)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Resources & References](#resources--references)

---

## What Happened?

On **March 31, 2026**, Anthropic accidentally leaked the **entire source code** of their popular AI coding assistant **Claude Code** through their npm registry. The leak occurred when a **59.8 MB source map file (`.map`)** was inadvertently included in version 2.1.88 of the `@anthropic/claude-code` npm package.

This incident exposed approximately **512,000+ lines** of TypeScript source code, revealing internal architectures, secret features, system prompts, and development tools that Anthropic had never intended to make public.

> **BREAKING**: The entire proprietary source code of one of the most popular AI coding assistants has been exposed to the public.

---

## The Technical Details

### How Source Maps Work

Source maps are debugging artifacts generated during the build process. They create a mapping between:

```
Minified Production Code <-> Original Source Code
```

### Why This Leak Happened

The source map file contained a critical field called `sourcesContent` - an array that embeds the **entire original source code** of each file as plain text strings within a JSON structure:

```json
{
  "version": 3,
  "file": "bundle.js",
  "sources": ["../src/main.ts", "../src/tools/..."],
  "sourcesContent": [
    "// All your original TypeScript code here",
    "// Every file, comment, and constant",
    "// Exposed in plain text"
  ],
  "mappings": "AAAA,SAAS,OAAO,CAAC,..."
}
```

### What Anthropic Missed

1. **No `.npmignore` file** to exclude source maps
2. **No `files` field** in `package.json` to whitelist allowed files
3. **Source maps in production builds** (should only be in development)

---

## Repository Contents

This repository contains **248 files** of source code and documentation:

| Directory | Description | Files |
|-----------|-------------|-------|
| `leaked-source/` | Original TypeScript source code from the leak | 87+ files |
| `clean-room-rust/spec/` | Behavioral specifications from code analysis | 15 files |
| `clean-room-rust/src-rust/` | Rust implementation of Claude Code behavior | 100+ files |
| `assets/` | Visual assets and banners | 2 files |
| Root | Documentation (README, LICENSE, etc.) | 6 files |

---

## Leaked Source Code

### Directory Structure

```
leaked-source/
├── assistant/
│   └── sessionHistory.ts          # Session management
├── bridge/
│   ├── bridgeApi.ts               # IDE Bridge API
│   ├── bridgeConfig.ts            # Bridge configuration
│   ├── bridgeDebug.ts             # Debug utilities
│   ├── bridgeEnabled.ts           # Enable/disable bridge
│   ├── bridgeMain.ts              # Main bridge logic
│   ├── bridgeMessaging.ts         # Message handling
│   ├── bridgePermissionCallbacks.ts
│   ├── bridgePointer.ts
│   ├── bridgeStatusUtil.ts        # Status utilities
│   ├── bridgeUI.ts               # UI components
│   ├── capacityWake.ts
│   ├── codeSessionApi.ts          # Code session API
│   ├── createSession.ts          # Session creation
│   ├── debugUtils.ts             # Debug utilities
│   ├── envLessBridgeConfig.ts
│   ├── flushGate.ts
│   ├── inboundAttachments.ts
│   ├── inboundMessages.ts
│   ├── initReplBridge.ts          # REPL bridge initialization
│   ├── jwtUtils.ts               # JWT utilities
│   ├── pollConfig.ts
│   ├── pollConfigDefaults.ts
│   ├── remoteBridgeCore.ts        # Remote bridge core
│   ├── replBridge.ts             # REPL bridge
│   ├── replBridgeHandle.ts
│   ├── replBridgeTransport.ts
│   ├── sessionIdCompat.ts
│   ├── sessionRunner.ts
│   ├── trustedDevice.ts
│   ├── types.ts                  # Type definitions
│   └── workSecret.ts
├── buddy/                        # Pet/Companion System
│   ├── CompanionSprite.tsx        # Sprite component
│   ├── companion.ts              # Companion logic
│   ├── prompt.ts                 # Companion prompts
│   ├── sprites.ts                # Sprite definitions
│   ├── types.ts                  # Companion types
│   └── useBuddyNotification.tsx
├── cli/
│   ├── exit.ts                   # Exit handling
│   ├── handlers/
│   │   ├── agents.ts             # Agent handlers
│   │   ├── auth.ts              # Authentication
│   │   ├── autoMode.ts          # Auto mode
│   │   ├── mcp.tsx              # MCP handlers
│   │   ├── plugins.ts           # Plugin system
│   │   └── util.tsx             # Utilities
│   ├── ndjsonSafeStringify.ts
│   ├── print.ts                  # Print utilities
│   ├── remoteIO.ts              # Remote I/O
│   ├── structuredIO.ts          # Structured I/O
│   └── transports/
│       └── HybridTransport.ts    # Hybrid transport
└── [More files in cli/ directory]
```

### Key Files Overview

#### `assistant/sessionHistory.ts`
- Session history management
- Stores conversation context

#### `bridge/` - IDE Bridge System
- **Purpose**: Bidirectional communication between IDE and CLI
- **Features**: VS Code extension, JetBrains plugin support
- **Security**: JWT-authenticated channels

#### `buddy/` - The Pet System
- Virtual companion with mood tracking
- Hunger, happiness, energy metrics
- ASCII sprite-based UI

#### `cli/` - Command Line Interface
- Main CLI entry points
- Handler system for different commands
- Transport layer for communication

---

## Clean Room Rust Implementation

### Overview

A Rust-based clean-room rewrite based on behavioral analysis of the leaked code.

### Directory Structure

```
clean-room-rust/
├── spec/                         # Behavioral Specifications
│   ├── 00_overview.md           # System overview
│   ├── 01_core_entry_query.md   # Core query handling
│   ├── 02_commands.md           # Command system
│   ├── 03_tools.md              # Tool definitions
│   ├── 04_components_core_messages.md
│   ├── 05_components_agents_permissions_design.md
│   ├── 06_services_context_state.md
│   ├── 07_hooks.md              # Hook system
│   ├── 08_ink_terminal.md       # Terminal UI
│   ├── 09_bridge_cli_remote.md  # Bridge system
│   ├── 10_utils.md              # Utilities
│   ├── 11_special_systems.md    # Special features
│   ├── 12_constants_types.md    # Constants & types
│   ├── 13_rust_codebase.md      # Rust implementation
│   └── INDEX.md                 # Specification index
│
└── src-rust/
    └── crates/
        ├── api/                 # API definitions
        ├── bridge/              # Bridge implementation
        ├── buddy/               # Pet system
        ├── cli/                 # CLI entry point
        ├── commands/            # Command handlers
        ├── core/                # Core functionality
        │   ├── analytics.rs
        │   ├── attachments.rs
        │   ├── auto_mode.rs
        │   ├── bash_classifier.rs
        │   ├── claudemd.rs
        │   ├── cloud_session.rs
        │   └── crypto_utils.rs
        └── [More modules]
```

---

## Key Discoveries

### The "Pet" System (Tamagotchi-Style)

One of the most surprising discoveries was a complete virtual pet system:

```typescript
interface PetState {
  name: string;
  species: 'cat' | 'dog' | 'custom';
  hunger: number;      // 0-100
  happiness: number;  // 0-100
  energy: number;     // 0-100
  mood: 'happy' | 'neutral' | 'sad' | 'excited';
}
```

### IDE Bridge System

Real-time bidirectional communication system:
- VS Code extension integration
- JetBrains plugin support
- JWT authentication

### Multi-Agent Architecture

Revealed a multi-agent orchestration system that had been quietly developing since August 2024.

---

## Timeline of Events

| Time | Event |
|------|-------|
| March 31, 2026 09:00 UTC | Version 2.1.88 published to npm |
| March 31, 2026 13:00 UTC | Chaofan Shou discovers the leak |
| March 31, 2026 13:30 UTC | News spreads on Twitter/X |
| March 31, 2026 14:00 UTC | GitHub repositories created |
| March 31, 2026 15:00 UTC | Claw-code reaches 100K stars |
| March 31, 2026 18:00 UTC | Anthropic confirms the leak |
| March 31, 2026 20:00 UTC | Compromised npm version removed |

---

## Security Implications

### What's NOT Affected

| Concern | Status |
|---------|--------|
| Customer Data | Safe - No customer data in source |
| API Keys | Safe - No production keys exposed |
| Model Weights | Safe - AI models not in source |
| User Conversations | Safe - Not stored in source |

### What's Affected

| Concern | Impact |
|---------|--------|
| Intellectual Property | Competitors now have blueprint |
| Unreleased Features | Future product differentiation |
| Internal Processes | Development methodology exposed |
| Security Practices | Internal tooling revealed |

---

## Frequently Asked Questions

### Q: Is the source code still available?
**A:** Yes! This repository contains the original leaked TypeScript source code.

### Q: Can I use this code commercially?
**A:** No. The code is copyrighted by Anthropic. Using it commercially would likely constitute copyright infringement.

### Q: What's in the Rust implementation?
**A:** A clean-room rewrite inspired by the behavioral analysis of the leaked code.

### Q: What makes this significant?
**A:** One of the most significant tech leaks in AI history, giving unprecedented access to how a leading AI company builds products.

---

## Resources & References

### News Coverage
- [The Verge](https://www.theverge.com/ai-artificial-intelligence/904776/anthropic-claude-source-code-leak)
- [Ars Technica](https://arstechnica.com/ai/2026/03/entire-claude-code-cli-source-code-leaks-thanks-to-exposed-map-file/)
- [VentureBeat](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know)
- [BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/claude-code-source-code-accidentally-leaked-in-npm-package/)

---

## Contributing

Contributions welcome! Help document this historic leak.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## License

This documentation is for educational purposes. The original Claude Code source code is property of Anthropic, PBC.

---

<div align="center">

### Star this repository!

**Help others discover this historic leak documentation.**

</div>

---

<p align="center">
  Last updated: April 2, 2026 | Maintained by the community
</p>
