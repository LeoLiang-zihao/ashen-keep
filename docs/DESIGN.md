# Ashen Keep Design

Ashen Keep is designed as a Python library first and a command-line game second. The CLI is intentionally thin so that the game rules can be tested directly.

## Core flow

1. `generation.py` creates a seeded dungeon and initial player.
2. `engine.py` exposes actions such as move, take item, and combat action.
3. `combat.py` resolves attack, defend, and potion turns.
4. `rendering.py` formats state and action results.
5. `cli.py` parses text commands and calls the engine.

## Scope choices

The first version has one dungeon floor, a small branching room graph, simple automatic equipment upgrades, healing potions, and one boss. This keeps the project small enough to test and document well.

## Extension points

Future versions could add normal/hard difficulty, adaptive scaling, more room events, more items, and richer procedural generation.
