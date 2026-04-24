# Ashen Keep Design Spec

Date: 2026-04-24

## Summary

Ashen Keep is a small AI-assisted Python roguelike-lite library with a thin command-line interface. The player explores a small branching dungeon called Slop Keep, gathers simple supplies, fights monsters in turn-based combat, and wins by defeating the boss. The default game should be easy enough to complete during a short demo, while the code structure should leave room for future difficulty modes.

The project prioritizes course development practices: readable Python code, Ruff style checks, tests, documentation, a clear library/interface split, GitHub issues, pull requests, and explicit documentation of generative AI usage.

## Goals

- Build a Python library that owns the game rules and state transitions.
- Provide a CLI that delegates to the library instead of embedding business logic.
- Keep the default game easy to play and easy to manually verify.
- Support seeded randomness so tests and demos can reproduce dungeon layouts.
- Include enough flavor text and small ASCII art to feel distinct without requiring external assets.
- Document setup, gameplay, testing, architecture, and AI usage.

## Non-Goals

- No graphical UI, image assets, sound, or external art pipeline.
- No complex inventory management.
- No multi-floor dungeon for the initial version.
- No large adaptive difficulty system in the initial version; it can remain a future extension.
- No hidden dependency on the CLI for tests of core game behavior.

## Project Identity

- Project/repository name: `ashen-keep`
- Python package name: `ashen_keep`
- Game title: Ashen Keep
- In-game dungeon name: Slop Keep
- Tone: classic fantasy dungeon with a subtle iron-gray fortress, ration, archive, banner, and bureaucratic ruin atmosphere. The project should not directly reference real-world political entities.

## Proposed Repository Structure

```text
ashen-keep/
  README.md
  pyproject.toml
  docs/
    AI_USAGE.md
    DESIGN.md
    superpowers/
      specs/
        2026-04-24-ashen-keep-design.md
  src/
    ashen_keep/
      __init__.py
      __main__.py
      cli.py
      combat.py
      content.py
      engine.py
      generation.py
      models.py
      rendering.py
  tests/
    test_combat.py
    test_engine.py
    test_generation.py
    test_items.py
    test_cli_smoke.py
```

## Architecture

### `models.py`

Defines plain game data structures:

- `Player`
- `Monster`
- `Item`
- `Room`
- `GameState`
- `DifficultyConfig`

These models should avoid direct terminal input/output.

### `generation.py`

Creates a small branching dungeon from a seed and difficulty config. It must guarantee:

- a fixed starting room,
- a reachable boss room,
- a short main path,
- a few optional side rooms,
- seeded reproducibility,
- easy default balance.

Recommended generation strategy:

1. Create a guaranteed main path of about five rooms.
2. Add three or four side rooms connected to main path rooms.
3. Place monsters and items in eligible rooms.
4. Place the boss in the final boss room.
5. Use `random.Random(seed)` rather than global randomness.

### `combat.py`

Owns combat rules for these player actions:

- `attack`
- `defend`
- `potion`

The module should return structured results or messages that the engine/renderer can display. It should not read from `input()` or print directly.

### `engine.py`

Coordinates game state transitions. The initial public API will expose:

- `start_game(seed: int | None = None, difficulty: str = "easy") -> GameState`
- `move(state: GameState, direction: str) -> ActionResult`
- `take_item(state: GameState) -> ActionResult`
- `perform_combat_action(state: GameState, action: str) -> ActionResult`
- `get_available_commands(state: GameState) -> list[str]`

The engine is the main API tested by unit tests.

### `content.py`

Contains text data:

- room names and descriptions,
- monster templates,
- item templates,
- boss description,
- title ASCII art,
- victory and defeat text.

This is where the project gets its distinct flavor without requiring external assets.

### `rendering.py`

Converts game state and action results into CLI-readable text. It should not mutate game state.

### `cli.py` and `__main__.py`

Provide the command loop:

- parse player commands,
- call engine functions,
- print rendered output,
- handle `help`, `look`, `status`, and `quit`.

The CLI should stay thin so the library remains testable.

## Gameplay Rules

### Main Loop

1. Start a new easy game.
2. Show title art and the starting room.
3. Accept commands such as `look`, `move north`, `n`, `take`, `attack`, `defend`, `potion`, `status`, `help`, and `quit`.
4. Prevent movement out of a room while a living monster is present.
5. Let the player collect items after clearing or entering rooms.
6. End with victory when the boss is defeated.
7. End with defeat when player HP reaches zero.

### Combat

Player stats:

- max HP,
- current HP,
- attack,
- defense,
- potion count,
- weapon name,
- armor name.

Monster stats:

- name,
- HP,
- attack,
- defense,
- boss flag.

Actions:

- `attack`: player damages the monster; if the monster survives, it counterattacks.
- `defend`: player skips attacking and receives reduced incoming damage for that turn.
- `potion`: player consumes one potion and heals; if the monster survives, it attacks.

Damage should be simple and deterministic enough to test with seeded randomness, for example:

```python
damage = max(1, attacker.attack + random_bonus - defender.defense)
```

### Items

Initial item scope:

- Healing items: `Healing Potion`, `Ration Flask`.
- Weapons: `Iron Sword`, `Quartermaster's Sabre`.
- Armor/shields: `Worn Shield`, `Stamped Buckler`.

Items should be simple:

- potions increase the player's potion count,
- better weapons automatically replace weaker weapons,
- better armor automatically replaces weaker armor,
- no complex backpack UI.

## Difficulty

The default mode is easy. It should favor quick completion and demo reliability.

Example easy configuration:

```python
DifficultyConfig(
    name="easy",
    room_count=9,
    monster_chance=0.45,
    item_chance=0.60,
    player_hp=32,
    player_attack=6,
    player_defense=1,
    starting_potions=2,
    monster_hp_range=(6, 12),
    boss_hp_range=(18, 24),
)
```

Future extension points:

- `normal` difficulty,
- `hard` difficulty,
- adaptive scaling based on player performance or dungeon depth.

The first implementation will include `easy`. `normal`, `hard`, and adaptive scaling are documented extension points rather than required initial features.

## Content Direction

Potential room names:

- Gatehouse of Ash
- Ration Hall
- Stamped Archive
- Banner Gallery
- Quartermaster's Vault
- Iron Chapel
- Redoubt of the Last Warden

Potential monsters:

- Hungry Goblin
- Dust-Bound Guard
- Ledger Imp
- Banner Wraith
- Rust Knight

Boss:

- The Last Warden

Potential items:

- Ration Flask
- Stamped Buckler
- Iron Sword
- Quartermaster's Sabre

Small ASCII title art is allowed and encouraged. No external visual assets are required.

## Testing Strategy

Tests should cover the library more than the CLI.

Recommended tests:

- Dungeon generation creates the requested number of rooms.
- Dungeon generation always creates a reachable boss room.
- The same seed creates the same dungeon layout.
- Player cannot move through invalid exits.
- Player cannot leave a room with a living monster.
- `attack` reduces monster HP.
- defeated monsters stop blocking movement.
- `defend` reduces incoming damage.
- `potion` heals and consumes one potion.
- taking a potion increases potion count.
- taking better equipment updates player stats.
- defeating the boss sets the game to victory.
- player death sets the game to defeat.
- CLI smoke test can run `--help` or a short command path without crashing.

Test command documented in README:

```bash
pytest
```

Style and quality commands documented in README:

```bash
ruff check src tests
ruff format --check src tests
mypy src tests
```

## Documentation Plan

### `README.md`

Should include:

- project summary,
- architecture overview,
- installation/setup,
- how to run the game,
- available commands,
- how to run tests,
- how to run style/type checks,
- short gameplay transcript,
- link to AI usage documentation.

### `docs/DESIGN.md`

A student-facing architecture summary derived from this spec.

### `docs/AI_USAGE.md`

Must document generative AI usage exhaustively, including:

- tools used,
- how each tool was used,
- what each tool produced,
- what the student reviewed or changed,
- that final responsibility remains with the student.

## GitHub Issue Plan

Suggested initial issues:

1. Set up Python package, Ruff, pytest, mypy, and README skeleton.
2. Implement core models for player, monster, room, item, and game state.
3. Implement seeded dungeon generation with reachable boss room.
4. Implement combat actions: attack, defend, and potion.
5. Implement item pickup and equipment upgrades.
6. Implement engine API for movement, commands, win, and loss states.
7. Implement CLI command loop and rendering.
8. Add tests for generation, combat, items, and engine behavior.
9. Write user documentation and gameplay transcript.
10. Document generative AI usage.

Because this is a solo project, all issues can be assigned to the single student. Pull requests should be used for reviewable chunks when practical, especially for setup, core engine, CLI, and documentation milestones.

## Risks and Mitigations

- Risk: scope grows too large.
  - Mitigation: keep one floor, simple items, and easy default difficulty.
- Risk: manual playtesting takes too long.
  - Mitigation: easy-by-default balance and seeded demo command.
- Risk: CLI becomes tangled with game logic.
  - Mitigation: engine and combat modules own state changes; CLI only parses commands.
- Risk: AI usage documentation is incomplete.
  - Mitigation: maintain `docs/AI_USAGE.md` while developing, not only at the end.

## Approval Status

The user approved:

- roguelike-lite direction,
- solo scope,
- boss victory condition,
- attack/defend/potion combat,
- classic fantasy theme,
- easy-by-default design,
- small branching graph dungeon,
- potions plus simple equipment,
- subtle non-generic fortress/archive/ration flavor,
- small ASCII/text flavor only,
- new repository under `~/projects`,
- `Ashen Keep` as project name and `Slop Keep` as in-game dungeon name,
- data-driven library architecture.
