# Feature Flag Analysis

This directory contains detailed documentation of the 44 feature flags discovered in Claude Code's leaked source code, documenting over 20 unreleased capabilities.

## Documentation Index

| Document | Description | Features |
|----------|-------------|----------|
| `feature-flag-reference.md` | Complete flag reference | 44 flags catalog |
| `kairos-system.md` | Always-on autonomous mode | KAIROS, proactive agent |
| `buddy-system.md` | Companion pet system | BUDDY, 18 species, gacha |
| `ultraplan-system.md` | Remote 30-min planning | ULTRAPLAN, CCR sessions |

## Key Unreleased Features

### Autonomous Systems

- **KAIROS**: Always-on background agent watching your work
- **ULTRAPLAN**: Offload complex planning to cloud runtime
- **autoDream**: Background memory consolidation

### Entertainment & Gamification

- **BUDDY**: Tamagotchi-style companion pets
- **Gacha System**: 18 species with rarity tiers
- **ASCII Sprites**: Animated pet characters

### Anti-Competitive Features

- **Anti-Distillation**: Poison competitor training data
- **Undercover Mode**: Hide Anthropic employee identity

## Feature Flag Overview

| Flag | Feature | Status |
|------|---------|--------|
| `KAIROS` | Autonomous daemon mode | Unreleased |
| `BUDDY` | Pet companion system | April 2026 launch |
| `ULTRAPLAN` | Remote planning | Unreleased |
| `UNDERCOVER` | Anti-leak protection | Active |
| `ANTI_DISTILLATION_CC` | Training poison | Active |
| `REDACT_THINKING` | Redacted reasoning | Beta |
| `AFK_MODE` | Background work | Unreleased |
| `CONTEXT_1M` | 1M token context | Unreleased |

## Usage

Each document can be read independently. Start with:

1. `feature-flag-reference.md` for complete catalog
2. System-specific documents for detailed analysis

## Note

Feature flags are compile-time constants in the source code. Their actual availability depends on Anthropic's internal build configuration and rollout schedule.
