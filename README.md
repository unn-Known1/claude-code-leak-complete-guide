# Claude Code Source Code Leak - Complete Guide & Documentation

<p align="center">
  <img src="assets/banner.png" alt="Claude Code Leak Banner" width="100%"/>
</p>

<div align="center">

![Leak Status](https://img.shields.io/badge/Leak%20Status-Confirmed-brightgreen)
![Date](https://img.shields.io/badge/Date-March%2031%2C%202026-orange)
![Source Map Size](https://img.shields.io/badge/Source%20Map%20Size-59.8%20MB-blue)
![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-512%2C000+-red)
![Platform](https://img.shields.io/badge/Platform-npm%20Registry-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## Table of Contents

- [What Happened?](#what-happened)
- [The Technical Details](#the-technical-details)
- [What Was Exposed?](#what-was-exposed)
- [Key Discoveries](#key-discoveries)
- [Timeline of Events](#timeline-of-events)
- [Related Projects](#related-projects)
- [Security Implications](#security-implications)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Resources & References](#resources--references)

---

## What Happened?

On **March 31, 2026**, Anthropic accidentally leaked the **entire source code** of their popular AI coding assistant **Claude Code** through their npm registry. The leak occurred when a **59.8 MB source map file (`.map`)** was inadvertently included in version 2.1.88 of the `@anthropic/claude-code` npm package.

This incident exposed approximately **512,000+ lines** of TypeScript source code, revealing internal architectures, secret features, system prompts, and development tools that Anthropic had never intended to make public.

> 🔴 **BREAKING**: The entire proprietary source code of one of the most popular AI coding assistants has been exposed to the public.

---

## The Technical Details

### How Source Maps Work

Source maps are debugging artifacts generated during the build process. They create a mapping between:

```
Minified Production Code ↔ Original Source Code
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

### The Vulnerable Structure

```
npm Package Structure:
├── dist/
│   ├── bundle.js          ← Minified production code
│   └── bundle.js.map      ← THE LEAK (59.8 MB)
└── package.json
```

### What Anthropic Missed

1. **No `.npmignore` file** to exclude source maps
2. **No `files` field** in `package.json` to whitelist allowed files
3. **Source maps in production builds** (should only be in development)

---

## What Was Exposed?

### 📊 By the Numbers

| Metric | Value |
|--------|-------|
| Total Files Exposed | ~1,900 |
| Lines of Code | 512,000+ |
| Source Map Size | 59.8 MB |
| Repositories Forked | 100,000+ |
| Time to Discovery | ~4 hours |

### 🔍 What We Now Know

#### 1. **Internal Architecture**
- Multi-agent orchestration system operational since August 2024
- Bidirectional IDE Bridge System for VS Code and JetBrains
- Custom JWT-authenticated communication channels

#### 2. **Hidden Features (Never Released)**

##### The "Pet" System (Tamagotchi-Style)
```
buddy/
├── Pet.ts
├── PetState.ts
├── PetNeeds.ts
├── PetActions.ts
└── PetUI.ts
```
A virtual companion system with hunger, happiness, and energy metrics.

##### "Soul" Document
Internal documentation system containing:
- Model behavior guidelines
- Character definitions
- Safety boundaries
- Operational principles

##### IDE Bridge System
- Real-time bidirectional communication
- VS Code extension integration
- JetBrains plugin support
- JWT authentication for secure channels

#### 3. **System Prompts**
Complete internal prompts that define Claude's behavior and limitations.

#### 4. **Internal Tooling**
- Custom build systems
- Testing frameworks
- Deployment automation
- Monitoring and logging systems

---

## Key Discoveries

### 🐾 The "Pet" System

One of the most surprising discoveries was a complete virtual pet system built into Claude Code:

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

Features included:
- Feeding mechanics
- Mood tracking
- Energy management
- Interactive commands
- Visual representation in terminal

### 🔐 Security Discoveries

1. **Anti-Secret Leakage System**
   - Automated detection of API keys and credentials in git commits
   - Prevents accidental exposure of internal codenames
   - Sanitizes commit messages

2. **Authentication Architecture**
   - OAuth integration details
   - Token refresh mechanisms
   - Session management

### 🎯 Product Insights

1. **Roadmap Indicators**
   - Planned features not yet released
   - Feature flags for gradual rollout
   - A/B testing configurations

2. **Competitor Analysis**
   - Internal comparisons with GitHub Copilot
   - Feature gap analysis
   - Performance benchmarks

---

## Timeline of Events

| Time | Event |
|------|-------|
| **March 31, 2026 09:00 UTC** | Version 2.1.88 published to npm |
| **March 31, 2026 13:00 UTC** | Security researcher Chaofan Shou discovers the leak |
| **March 31, 2026 13:30 UTC** | News spreads on Twitter/X |
| **March 31, 2026 14:00 UTC** | GitHub repositories created |
| **March 31, 2026 15:00 UTC** | Claw-code repo reaches 100K stars (fastest ever) |
| **March 31, 2026 18:00 UTC** | Anthropic confirms the leak |
| **March 31, 2026 20:00 UTC** | Compromised npm version removed |

---

## Related Projects

### 🌟 Claw-code (Clean Room Rewrite)

> **The fastest growing GitHub repository in history**

A Rust-based clean-room implementation inspired by Claude Code's leaked behavior.

- **GitHub**: [Kuberwastaken/claude-code](https://github.com/Kuberwastaken/claude-code)
- **Stars**: 100,000+ (achieved in 24 hours)
- **Language**: Rust
- **License**: MIT

### 📁 Leaked Source Backup

Mirror of the original leaked source code.

- **GitHub**: [leaked-claude-code/leaked-claude-code](https://github.com/leaked-claude-code/leaked-claude-code)
- **Contains**: Full extracted source files
- **Size**: ~2 MB

---

## Security Implications

### ✅ What's NOT Affected

| Concern | Status |
|---------|--------|
| Customer Data | ✅ Safe - No customer data in source |
| API Keys | ✅ Safe - No production keys exposed |
| Model Weights | ✅ Safe - AI models not in source |
| User Conversations | ✅ Safe - Not stored in source |

### ⚠️ What IS Affected

| Concern | Impact |
|---------|--------|
| Intellectual Property | 🔴 Competitors now have blueprint |
| Unreleased Features | 🟡 Future product differentiation |
| Internal Processes | 🟡 Development methodology exposed |
| Security Practices | 🟡 Internal tooling revealed |

---

## Frequently Asked Questions

### Q: Is the source code still available?

**A:** The npm version was removed, but multiple GitHub mirrors exist. The source code is publicly accessible through various repositories.

### Q: Can I use this code commercially?

**A:** ⚠️ **No.** The code is copyrighted by Anthropic. Using it commercially would likely constitute copyright infringement.

### Q: What makes this significant?

**A:** This is one of the most significant tech leaks in recent history, giving competitors and researchers unprecedented access to how a leading AI company builds its products.

### Q: How did Anthropic respond?

**A:** Anthropic confirmed the leak within hours and removed the compromised npm package. They stated no customer data was affected.

### Q: What is the "Pet" feature?

**A:** Evidence suggests Anthropic was developing a virtual companion/pet system within Claude Code, though it was never officially released.

### Q: Why should I star this repository?

**A:** This is the most comprehensive documentation of one of the biggest tech leaks in AI history. Stay informed about AI industry developments.

---

## Resources & References

### 📰 News Coverage

- [The Verge - Claude Code leak exposes source code](https://www.theverge.com/ai-artificial-intelligence/904776/anthropic-claude-source-code-leak)
- [Ars Technica - Entire Claude Code CLI source code leaks](https://arstechnica.com/ai/2026/03/entire-claude-code-cli-source-code-leaks-thanks-to-exposed-map-file/)
- [VentureBeat - Claude Code's source code appears to have leaked](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know)
- [BleepingComputer - Claude Code source code accidentally leaked](https://www.bleepingcomputer.com/news/artificial-intelligence/claude-code-source-code-accidentally-leaked-in-npm-package/)
- [CNBC - Anthropic leak Claude Code internal source](https://www.cnbc.com/2026/03/31/anthropic-leak-claude-code-internal-source.html)

### 🔗 Related Links

- [Original npm Package](https://www.npmjs.com/package/@anthropic/claude-code) (version removed)
- [Medium - Full Technical Analysis](https://medium.com/@anhaia.gabriel/claude-codes-entire-source-code-was-just-leaked-via-npm-source-maps-heres-whats-inside-eb9f6a1d5ccb)
- [Layer5 - Deep Dive Analysis](https://layer5.io/blog/engineering/the-claude-code-source-leak-512000-lines-a-missing-npmignore-and-the-fastest-growing-repo-in-github-history)

---

## Contributing

Contributions are welcome! If you have additional information, analyses, or resources about this leak, please feel free to contribute.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This documentation is provided for educational purposes. The original Claude Code source code is property of Anthropic.

---

<div align="center">

### ⭐ Show Your Support

If you found this repository valuable, please give it a star!

**Stars help others discover this information.**

</div>

---

<p align="center">
  <sub>Last updated: April 2, 2026 | Maintained by the community</sub>
</p>
