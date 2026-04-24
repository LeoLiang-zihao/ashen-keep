# Ashen Keep

Ashen Keep is a small Python roguelike-lite library and command-line game. The player explores Slop Keep, a compact branching dungeon, collects simple supplies, fights monsters, and wins by defeating The Last Warden.

The project is intentionally small: it focuses on clean architecture, tests, style consistency, documentation, and a clear separation between the underlying Python library and the CLI interface.

## Architecture

The library lives in `src/ashen_keep`:

- `models.py`: player, monster, item, room, game state, and action result data models.
- `content.py`: static room, item, monster, difficulty, and flavor text content.
- `generation.py`: seeded dungeon generation.
- `combat.py`: attack, defend, and potion combat actions.
- `engine.py`: public game-state API used by tests and the CLI.
- `rendering.py`: turns game state into display text.
- `cli.py`: thin command-line interface.

The CLI delegates to the library. Core rules are testable without interactive input.

## Setup

Clone the repository, create a virtual environment, and install development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Run the game

```bash
python -m ashen_keep
```

For a reproducible demo run:

```bash
python -m ashen_keep --demo
```

or:

```bash
python -m ashen_keep --seed 7
```

## Commands

Inside the game:

- `look`: show the current room again
- `status`: show HP, attack, defense, equipment, and potions
- `move north`, `move east`, `move south`, `move west`: move through exits
- `n`, `e`, `s`, `w`: short movement commands
- `take`: pick up the first item in the room
- `attack`: attack the current monster
- `defend`: guard against the current monster
- `potion`: drink a healing potion
- `help`: show command help
- `quit`: leave the game

## Run tests

```bash
pytest
```

## Run style and type checks

```bash
ruff check src tests
ruff format --check src tests
mypy src tests
```

## Development practices

This project uses:

- Ruff for style consistency.
- Pytest for automated tests.
- Mypy for static type checking.
- GitHub issues for development tasks.
- Pull requests for reviewable work chunks when practical.

## Generative AI usage

Generative AI usage is documented in [`docs/AI_USAGE.md`](docs/AI_USAGE.md).
