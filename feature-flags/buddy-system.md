# BUDDY - Tamagotchi Companion System

## Overview

BUDDY is a gamified companion pet system for Claude Code, inspired by Tamagotchi virtual pets. It was planned as an April 1, 2026 teaser with full launch in May 2026.

## System Design

### Core Concept

Users can hatch and raise companion pets that live in the terminal alongside Claude Code, providing:

1. **Entertainment**: Cute ASCII art companions
2. **Stats**: Five procedurally generated stats
3. **Rarity System**: Gacha-based species acquisition
4. **Animations**: Multi-frame sprite animations

### Species Catalog

18 species across 5 rarity tiers:

| Rarity | Chance | Species |
|--------|--------|---------|
| Common | 60% | Pebblecrab, Dustbunny, Mossfrog, Twigling, Dewdrop, Puddlefish |
| Uncommon | 25% | Cloudferret, Gustowl, Bramblebear, Thornfox |
| Rare | 10% | Crystaldrake, Deepstag, Lavapup |
| Epic | 4% | Stormwyrm, Voidcat, Aetherling |
| Legendary | 1% | Cosmoshale, Nebulynx |

### Shiny Variants

Each species has a 1% chance of being Shiny:
- **Base species**: 1% shiny chance
- **Legendary**: 0.01% shiny chance (10x rarer)

## Gacha System

### Mechanics

The gacha system uses deterministic randomization:

```typescript
// Seeded PRNG using Mulberry32
function rollBuddy(userId: string): Buddy {
  const seed = hash(userId);
  const rng = new Mulberry32(seed);

  // Roll rarity
  const rarityRoll = rng.random();
  const rarity = getRarity(rarityRoll);

  // Roll species within rarity
  const species = pickSpecies(rarity, rng);

  // Roll shiny
  const shinyRoll = rng.random();
  const isShiny = shinyRoll < 0.01;

  // Generate stats
  const stats = generateStats(rng);

  return { rarity, species, isShiny, stats };
}
```

### Rarity Thresholds

```typescript
const RARITY_THRESHOLDS = {
  COMMON: 0.60,      // 0.00 - 0.60
  UNCOMMON: 0.25,    // 0.60 - 0.85
  RARE: 0.10,         // 0.85 - 0.95
  EPIC: 0.04,         // 0.95 - 0.99
  LEGENDARY: 0.01,   // 0.99 - 1.00
};
```

## Stats System

Each Buddy has 5 procedurally generated stats:

| Stat | Description | Range |
|------|-------------|-------|
| `DEBUGGING` | Problem-solving ability | 1-100 |
| `PATIENCE` | Tolerance for repetitive tasks | 1-100 |
| `CHAOS` | Tendency for creative solutions | 1-100 |
| `WISDOM` | Code quality awareness | 1-100 |
| `SNARK` | Wit and humor level | 1-100 |

### Stat Generation

```typescript
function generateStats(rng: PRNG): Stats {
  return {
    DEBUGGING: Math.floor(rng.random() * 100) + 1,
    PATIENCE: Math.floor(rng.random() * 100) + 1,
    CHAOS: Math.floor(rng.random() * 100) + 1,
    WISDOM: Math.floor(rng.random() * 100) + 1,
    SNARK: Math.floor(rng.random() * 100) + 1,
  };
}
```

## ASCII Art Sprites

### Format

Each sprite is 5 lines tall, 12 characters wide:

```
# Sample Pebblecrab sprite
   ___
  /   \
 | 0 0 |
  \___/

# Sample Dustbunny sprite
  (\(\
  ( -.-)
  o_(")(")
```

### Animation Frames

Each species has multiple animation frames:

```typescript
interface BuddySprite {
  species: string;
  frames: string[][];  // Array of 5-line sprites
  animationSpeed: number;  // ms per frame
}
```

## Launch Timeline

| Date | Phase | Description |
|------|-------|-------------|
| 2026-04-01 | Teaser | Limited hatching available |
| 2026-04-07 | Teaser End | Teaser period ends |
| 2026-05-01 | Full Launch | Full system release |

### Launch Window

The BUDDY system checks if current date is within launch window:

```typescript
const LAUNCH_START = new Date('2026-04-01');
const LAUNCH_END = new Date('2026-04-07');
const FULL_LAUNCH = new Date('2026-05-01');

function isBuddyAvailable(): boolean {
  const now = new Date();

  if (now < LAUNCH_START) return false;
  if (now >= LAUNCH_START && now <= LAUNCH_END) return true;  // Teaser
  if (now >= FULL_LAUNCH) return true;  // Full launch

  return false;
}
```

## Feature Flag

```typescript
const BUDDY = true;  // Compile-time flag
```

### Environment Variable

```bash
# Enable BUDDY
CLAUDE_CODE_BUDDY=1
```

## Implementation Details

### Storage

Buddy data stored in:

```
.claude/buddy/
├── config.json      # User's buddy
├── sprites/         # Cached sprites
└── stats.json       # Historical stats
```

### Data Structure

```typescript
interface Buddy {
  id: string;
  species: string;
  rarity: Rarity;
  isShiny: boolean;
  stats: Stats;
  hatchedAt: Date;
  level: number;
  experience: number;
}

interface UserBuddyConfig {
  activeBuddy: Buddy | null;
  totalHatched: number;
  shiniesObtained: number;
}
```

## Sprite Examples

### Common Species

```
Pebblecrab:
   ___
  /   \
 | o o |
  \___/

Dustbunny:
  (\(\
  ( -.-)
  o_(")(")

Mossfrog:
 ~  ~
( oo )
 \__/
```

### Uncommon Species

```
Cloudferret:
  /\  /\
 ( oo )
  \__/~~

Gustowl:
  u_u
 /o o\
 |___|

Bramblebear:
  ___
 _/   \_
( @   @ )
 |  ^  |
 |_____|
```

### Legendary Species

```
Cosmoshale:
  *  *
 /|  |\
* |  | *
 \|  |/
  *  *

Nebulynx:
 /^   ^\
( o   o )
 \\_U_/
  /   \
```

## Gamification Features

### Experience System

- Gain XP for successful tasks
- Level up every 100 XP
- Higher levels unlock abilities

### Evolution (Future)

Not in initial release, but code suggests evolution system planned:

```typescript
// Referenced but not implemented
const EVOLUTION_THRESHOLDS = {
  'Pebblecrab': { level: 10, evolvesTo: 'Crystalcrab' },
  'Dustbunny': { level: 15, evolvesTo: 'Shadowbunny' },
};
```

## User Interface

### Commands

```bash
# Hatch a buddy
claude buddy hatch

# View your buddy
claude buddy view

# Check stats
claude buddy stats

# Feed your buddy
claude buddy feed
```

### In-Conversation

Users can mention their buddy:

```
User: "Hey, what does my buddy think?"
Claude: "Your Pebblecrab says it spotted a potential bug!"
```

## Privacy

Buddy data stays local:
- No server sync
- Local storage only
- User owns their data

## Easter Eggs

The source reveals potential future features:

- Seasonal variants
- Trading system
- Battle arena
- Custom sprites

These are not implemented in current version.
