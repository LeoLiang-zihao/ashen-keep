# Ashen Keep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Ashen Keep, a small tested Python roguelike-lite library with a thin CLI where the player explores Slop Keep and wins by defeating The Last Warden.

**Architecture:** Keep game logic in `src/ashen_keep` and keep the CLI thin. `models.py` defines data structures, `generation.py` creates reproducible dungeons, `combat.py` handles turn actions, `engine.py` coordinates game-state transitions, `rendering.py` formats state, and `cli.py` handles user input.

**Tech Stack:** Python 3.11+, pytest, ruff, mypy, standard library only for runtime.

---

## File Structure

Create these files:

- `pyproject.toml`: project metadata plus pytest, ruff, and mypy configuration.
- `README.md`: setup, gameplay, architecture, testing, and AI usage link.
- `docs/DESIGN.md`: concise student-facing architecture notes.
- `docs/AI_USAGE.md`: required exhaustive AI usage documentation.
- `src/ashen_keep/__init__.py`: public package exports and version.
- `src/ashen_keep/__main__.py`: `python -m ashen_keep` entry point.
- `src/ashen_keep/models.py`: dataclasses and small enums/literals for the game domain.
- `src/ashen_keep/content.py`: static text content, title art, room templates, item/monster templates, difficulty configs.
- `src/ashen_keep/generation.py`: seeded dungeon generation.
- `src/ashen_keep/combat.py`: attack/defend/potion combat resolution.
- `src/ashen_keep/engine.py`: public library API for starting games, moving, taking items, and combat actions.
- `src/ashen_keep/rendering.py`: convert `GameState` and `ActionResult` to display strings.
- `src/ashen_keep/cli.py`: command parser and interactive loop.
- `tests/test_generation.py`: dungeon generation tests.
- `tests/test_combat.py`: combat rules tests.
- `tests/test_engine.py`: movement, win/loss, and command tests.
- `tests/test_items.py`: item pickup/equipment tests.
- `tests/test_cli_smoke.py`: CLI entry smoke tests.

---

### Task 1: Project skeleton and tool configuration

**Files:**
- Create: `pyproject.toml`
- Create: `src/ashen_keep/__init__.py`
- Create: `tests/test_package.py`

- [ ] **Step 1: Create the package directories**

Run:

```bash
cd /Users/liangzihao/Projects/ashen-keep
mkdir -p src/ashen_keep tests docs
```

Expected: directories exist.

- [ ] **Step 2: Create `pyproject.toml`**

Write `pyproject.toml` exactly as:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "ashen-keep"
version = "0.1.0"
description = "A small Python roguelike-lite library and CLI."
readme = "README.md"
requires-python = ">=3.11"
authors = [
  { name = "Leo Liang" }
]
dependencies = []

[project.optional-dependencies]
dev = [
  "mypy>=1.8",
  "pytest>=8.0",
  "ruff>=0.4",
]

[project.scripts]
ashen-keep = "ashen_keep.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.ruff]
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = [
  "D",
  "E",
  "F",
  "I",
  "B",
  "SIM",
  "UP",
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["D100", "D101", "D102", "D103"]

[tool.mypy]
python_version = "3.11"
mypy_path = "src"
strict = true
warn_return_any = true
warn_unused_configs = true
```

- [ ] **Step 3: Create `src/ashen_keep/__init__.py`**

Write:

```python
"""Ashen Keep: a small roguelike-lite library and CLI."""

__version__ = "0.1.0"
```

- [ ] **Step 4: Write the first package test**

Create `tests/test_package.py`:

```python
from ashen_keep import __version__


def test_package_has_version() -> None:
    assert __version__ == "0.1.0"
```

- [ ] **Step 5: Run the package test**

Run:

```bash
python -m pytest tests/test_package.py -v
```

Expected: 1 passed.

- [ ] **Step 6: Run style check for current files**

Run:

```bash
python -m ruff check src tests
```

Expected: all checks passed.

- [ ] **Step 7: Commit**

Run:

```bash
git add pyproject.toml src/ashen_keep/__init__.py tests/test_package.py
git commit -m "chore: set up Ashen Keep package"
```

---

### Task 2: Core domain models

**Files:**
- Create: `src/ashen_keep/models.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Write failing model tests**

Create `tests/test_models.py`:

```python
from ashen_keep.models import (
    ActionResult,
    GameStatus,
    Item,
    ItemKind,
    Monster,
    Player,
    Room,
)


def test_player_alive_and_heal_clamps_to_max_hp() -> None:
    player = Player(max_hp=30, hp=10, attack=6, defense=1, potions=2)

    healed = player.heal(50)

    assert healed == 20
    assert player.hp == 30
    assert player.is_alive


def test_monster_alive_property() -> None:
    monster = Monster(name="Ledger Imp", max_hp=5, hp=0, attack=2, defense=0)

    assert not monster.is_alive


def test_room_detects_living_monster() -> None:
    room = Room(
        room_id="archive",
        name="Stamped Archive",
        description="Rows of stamped ledgers sag in the dust.",
        exits={"west": "gatehouse"},
        monster=Monster(name="Ledger Imp", max_hp=5, hp=5, attack=2, defense=0),
        items=[],
    )

    assert room.has_living_monster


def test_action_result_defaults_to_in_progress() -> None:
    result = ActionResult(message="You wait.")

    assert result.status == GameStatus.IN_PROGRESS


def test_item_has_kind_and_bonus() -> None:
    item = Item(name="Iron Sword", kind=ItemKind.WEAPON, bonus=2)

    assert item.kind is ItemKind.WEAPON
    assert item.bonus == 2
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/test_models.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'ashen_keep.models'`.

- [ ] **Step 3: Implement `models.py`**

Create `src/ashen_keep/models.py`:

```python
"""Core domain models for Ashen Keep."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class GameStatus(str, Enum):
    """Overall lifecycle status for a game."""

    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"
    QUIT = "quit"


class ItemKind(str, Enum):
    """Supported item categories."""

    POTION = "potion"
    WEAPON = "weapon"
    ARMOR = "armor"


@dataclass(slots=True)
class Item:
    """An item that can be collected in a room."""

    name: str
    kind: ItemKind
    bonus: int = 0
    heal_amount: int = 0
    description: str = ""


@dataclass(slots=True)
class Player:
    """Mutable player state."""

    max_hp: int
    hp: int
    attack: int
    defense: int
    potions: int
    weapon_name: str = "Rusty Sword"
    armor_name: str = "Threadbare Cloak"

    @property
    def is_alive(self) -> bool:
        """Return whether the player still has HP."""
        return self.hp > 0

    def heal(self, amount: int) -> int:
        """Heal by up to amount and return actual HP restored."""
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before


@dataclass(slots=True)
class Monster:
    """A hostile creature in a room."""

    name: str
    max_hp: int
    hp: int
    attack: int
    defense: int
    is_boss: bool = False
    description: str = ""

    @property
    def is_alive(self) -> bool:
        """Return whether the monster still has HP."""
        return self.hp > 0


@dataclass(slots=True)
class Room:
    """A dungeon room connected to other rooms by named exits."""

    room_id: str
    name: str
    description: str
    exits: dict[str, str] = field(default_factory=dict)
    monster: Monster | None = None
    items: list[Item] = field(default_factory=list)
    visited: bool = False

    @property
    def has_living_monster(self) -> bool:
        """Return whether this room contains a living monster."""
        return self.monster is not None and self.monster.is_alive


@dataclass(frozen=True, slots=True)
class DifficultyConfig:
    """Tunable game balance for dungeon generation and combat."""

    name: str
    room_count: int
    monster_chance: float
    item_chance: float
    player_hp: int
    player_attack: int
    player_defense: int
    starting_potions: int
    monster_hp_range: tuple[int, int]
    boss_hp_range: tuple[int, int]
    potion_heal: int


@dataclass(slots=True)
class GameState:
    """Complete mutable state for one game run."""

    player: Player
    rooms: dict[str, Room]
    current_room_id: str
    boss_room_id: str
    status: GameStatus = GameStatus.IN_PROGRESS
    seed: int | None = None
    difficulty: str = "easy"

    @property
    def current_room(self) -> Room:
        """Return the room the player currently occupies."""
        return self.rooms[self.current_room_id]


@dataclass(frozen=True, slots=True)
class ActionResult:
    """Structured result returned by engine and combat actions."""

    message: str
    status: GameStatus = GameStatus.IN_PROGRESS
```

- [ ] **Step 4: Run model tests**

Run:

```bash
python -m pytest tests/test_models.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Run ruff on new files**

Run:

```bash
python -m ruff check src/ashen_keep/models.py tests/test_models.py
```

Expected: all checks passed.

- [ ] **Step 6: Commit**

Run:

```bash
git add src/ashen_keep/models.py tests/test_models.py
git commit -m "feat: add core game models"
```

---

### Task 3: Static content and difficulty configuration

**Files:**
- Create: `src/ashen_keep/content.py`
- Create: `tests/test_content.py`

- [ ] **Step 1: Write failing content tests**

Create `tests/test_content.py`:

```python
from ashen_keep.content import (
    BOSS_TEMPLATE,
    DIFFICULTIES,
    ITEM_TEMPLATES,
    MONSTER_TEMPLATES,
    ROOM_TEMPLATES,
    TITLE_ART,
)
from ashen_keep.models import ItemKind


def test_easy_difficulty_is_default_friendly() -> None:
    easy = DIFFICULTIES["easy"]

    assert easy.room_count == 9
    assert easy.player_hp >= 30
    assert easy.starting_potions >= 2
    assert easy.potion_heal == 8


def test_content_has_enough_room_templates() -> None:
    assert len(ROOM_TEMPLATES) >= 9
    assert ROOM_TEMPLATES[0].room_id == "gatehouse"


def test_content_has_monsters_items_and_boss() -> None:
    assert len(MONSTER_TEMPLATES) >= 4
    assert len(ITEM_TEMPLATES) >= 4
    assert BOSS_TEMPLATE.is_boss
    assert any(item.kind is ItemKind.POTION for item in ITEM_TEMPLATES)
    assert any(item.kind is ItemKind.WEAPON for item in ITEM_TEMPLATES)
    assert any(item.kind is ItemKind.ARMOR for item in ITEM_TEMPLATES)


def test_title_art_names_game() -> None:
    assert "ASHEN KEEP" in TITLE_ART
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/test_content.py -v
```

Expected: FAIL with `ModuleNotFoundError` or missing attributes.

- [ ] **Step 3: Implement `content.py`**

Create `src/ashen_keep/content.py`:

```python
"""Static content and balance data for Ashen Keep."""

from __future__ import annotations

from dataclasses import dataclass

from ashen_keep.models import DifficultyConfig, Item, ItemKind, Monster

TITLE_ART = r"""
    _        _                 _  __               
   / \   ___| |__   ___ _ __  | |/ /___  ___ _ __  
  / _ \ / __| '_ \ / _ \ '_ \ | ' // _ \/ _ \ '_ \ 
 / ___ \\__ \ | | |  __/ | | || . \  __/  __/ |_) |
/_/   \_\___/_| |_|\___|_| |_||_|\_\___|\___| .__/ 
                                             |_|    
                  ASHEN KEEP
""".strip("\n")

VICTORY_TEXT = "The Last Warden falls. Slop Keep exhales dust and old orders."
DEFEAT_TEXT = "Your lamp gutters out beneath the stamped stones of Slop Keep."


@dataclass(frozen=True, slots=True)
class RoomTemplate:
    """Static room content used during generation."""

    room_id: str
    name: str
    description: str


ROOM_TEMPLATES: tuple[RoomTemplate, ...] = (
    RoomTemplate(
        "gatehouse",
        "Gatehouse of Ash",
        "A cold archway opens beneath torn banners and gray stone teeth.",
    ),
    RoomTemplate(
        "ration_hall",
        "Ration Hall",
        "Long tables wait in perfect rows, each marked by a chipped tin bowl.",
    ),
    RoomTemplate(
        "stamped_archive",
        "Stamped Archive",
        "Shelves of ledgers sag under seals no living clerk remembers.",
    ),
    RoomTemplate(
        "banner_gallery",
        "Banner Gallery",
        "Faded cloth hangs like captured dusk above the cracked floor.",
    ),
    RoomTemplate(
        "quartermaster_vault",
        "Quartermaster's Vault",
        "Locked crates split open around a desk carved with tally marks.",
    ),
    RoomTemplate(
        "iron_chapel",
        "Iron Chapel",
        "Iron votive stands line the walls, each bent toward a silent altar.",
    ),
    RoomTemplate(
        "barracks",
        "Dust-Bound Barracks",
        "Neat bunks remain made for soldiers who never returned to them.",
    ),
    RoomTemplate(
        "permit_office",
        "Permit Office",
        "A brass window divides the room, though no one waits in line now.",
    ),
    RoomTemplate(
        "redoubt",
        "Redoubt of the Last Warden",
        "A final chamber of blackened stone holds a throne, a ledger, and a blade.",
    ),
)

MONSTER_TEMPLATES: tuple[Monster, ...] = (
    Monster("Hungry Goblin", max_hp=7, hp=7, attack=3, defense=0),
    Monster("Ledger Imp", max_hp=6, hp=6, attack=2, defense=1),
    Monster("Dust-Bound Guard", max_hp=10, hp=10, attack=4, defense=1),
    Monster("Banner Wraith", max_hp=9, hp=9, attack=5, defense=0),
    Monster("Rust Knight", max_hp=12, hp=12, attack=4, defense=2),
)

BOSS_TEMPLATE = Monster(
    "The Last Warden",
    max_hp=22,
    hp=22,
    attack=5,
    defense=1,
    is_boss=True,
    description="A crowned jailer of old commands, still guarding a ruined chain.",
)

ITEM_TEMPLATES: tuple[Item, ...] = (
    Item(
        "Healing Potion",
        kind=ItemKind.POTION,
        heal_amount=8,
        description="A clear draught that closes fresh wounds.",
    ),
    Item(
        "Ration Flask",
        kind=ItemKind.POTION,
        heal_amount=8,
        description="A bitter flask from the quartermaster's emergency shelf.",
    ),
    Item(
        "Iron Sword",
        kind=ItemKind.WEAPON,
        bonus=2,
        description="A plain blade with a registry number etched near the hilt.",
    ),
    Item(
        "Quartermaster's Sabre",
        kind=ItemKind.WEAPON,
        bonus=3,
        description="A curved service blade, polished by someone very afraid.",
    ),
    Item(
        "Worn Shield",
        kind=ItemKind.ARMOR,
        bonus=1,
        description="A dented shield that still knows its duty.",
    ),
    Item(
        "Stamped Buckler",
        kind=ItemKind.ARMOR,
        bonus=2,
        description="A compact shield stamped with an unreadable seal.",
    ),
)

DIFFICULTIES: dict[str, DifficultyConfig] = {
    "easy": DifficultyConfig(
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
        potion_heal=8,
    )
}
```

- [ ] **Step 4: Run content tests**

Run:

```bash
python -m pytest tests/test_content.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Run ruff**

Run:

```bash
python -m ruff check src/ashen_keep/content.py tests/test_content.py
```

Expected: all checks passed.

- [ ] **Step 6: Commit**

Run:

```bash
git add src/ashen_keep/content.py tests/test_content.py
git commit -m "feat: add game content and difficulty config"
```

---

### Task 4: Seeded dungeon generation

**Files:**
- Create: `src/ashen_keep/generation.py`
- Create: `tests/test_generation.py`

- [ ] **Step 1: Write failing generation tests**

Create `tests/test_generation.py`:

```python
from collections import deque

from ashen_keep.generation import create_dungeon, create_player
from ashen_keep.models import GameStatus


def boss_is_reachable(state_room_ids: dict[str, list[str]], start: str, boss: str) -> bool:
    seen = {start}
    queue: deque[str] = deque([start])
    while queue:
        room_id = queue.popleft()
        if room_id == boss:
            return True
        for next_room_id in state_room_ids[room_id]:
            if next_room_id not in seen:
                seen.add(next_room_id)
                queue.append(next_room_id)
    return False


def test_create_player_uses_easy_config() -> None:
    player = create_player("easy")

    assert player.max_hp == 32
    assert player.hp == 32
    assert player.attack == 6
    assert player.defense == 1
    assert player.potions == 2


def test_create_dungeon_has_reachable_boss() -> None:
    state = create_dungeon(seed=7, difficulty="easy")
    graph = {
        room_id: list(room.exits.values()) for room_id, room in state.rooms.items()
    }

    assert state.status is GameStatus.IN_PROGRESS
    assert len(state.rooms) == 9
    assert state.current_room_id == "gatehouse"
    assert state.boss_room_id == "redoubt"
    assert boss_is_reachable(graph, state.current_room_id, state.boss_room_id)
    assert state.rooms[state.boss_room_id].monster is not None
    assert state.rooms[state.boss_room_id].monster.is_boss


def test_create_dungeon_is_seed_reproducible() -> None:
    first = create_dungeon(seed=11, difficulty="easy")
    second = create_dungeon(seed=11, difficulty="easy")

    first_exits = {room_id: room.exits for room_id, room in first.rooms.items()}
    second_exits = {room_id: room.exits for room_id, room in second.rooms.items()}
    first_items = {
        room_id: [item.name for item in room.items]
        for room_id, room in first.rooms.items()
    }
    second_items = {
        room_id: [item.name for item in room.items]
        for room_id, room in second.rooms.items()
    }

    assert first_exits == second_exits
    assert first_items == second_items


def test_unknown_difficulty_raises_value_error() -> None:
    try:
        create_dungeon(seed=1, difficulty="nightmare")
    except ValueError as error:
        assert "Unknown difficulty" in str(error)
    else:
        raise AssertionError("Expected ValueError")
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/test_generation.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'ashen_keep.generation'`.

- [ ] **Step 3: Implement `generation.py`**

Create `src/ashen_keep/generation.py`:

```python
"""Seeded dungeon generation for Ashen Keep."""

from __future__ import annotations

from copy import deepcopy
from random import Random

from ashen_keep.content import (
    BOSS_TEMPLATE,
    DIFFICULTIES,
    ITEM_TEMPLATES,
    MONSTER_TEMPLATES,
    ROOM_TEMPLATES,
)
from ashen_keep.models import GameState, Monster, Player, Room

DIRECTION_PAIRS: tuple[tuple[str, str], ...] = (
    ("north", "south"),
    ("east", "west"),
    ("south", "north"),
    ("west", "east"),
)
MAIN_PATH_IDS = (
    "gatehouse",
    "ration_hall",
    "stamped_archive",
    "iron_chapel",
    "redoubt",
)


def create_player(difficulty: str = "easy") -> Player:
    """Create a new player from a difficulty configuration."""
    config = _get_config(difficulty)
    return Player(
        max_hp=config.player_hp,
        hp=config.player_hp,
        attack=config.player_attack,
        defense=config.player_defense,
        potions=config.starting_potions,
    )


def create_dungeon(seed: int | None = None, difficulty: str = "easy") -> GameState:
    """Create a reproducible small branching dungeon."""
    config = _get_config(difficulty)
    rng = Random(seed)
    rooms = _create_empty_rooms(config.room_count)
    _connect_main_path(rooms)
    _connect_side_rooms(rooms, rng)
    _place_content(rooms, rng, difficulty)
    player = create_player(difficulty)
    rooms["gatehouse"].visited = True
    return GameState(
        player=player,
        rooms=rooms,
        current_room_id="gatehouse",
        boss_room_id="redoubt",
        seed=seed,
        difficulty=difficulty,
    )


def _get_config(difficulty: str):  # type: ignore[no-untyped-def]
    if difficulty not in DIFFICULTIES:
        known = ", ".join(sorted(DIFFICULTIES))
        raise ValueError(f"Unknown difficulty {difficulty!r}. Expected one of: {known}.")
    return DIFFICULTIES[difficulty]


def _create_empty_rooms(room_count: int) -> dict[str, Room]:
    selected_templates = ROOM_TEMPLATES[:room_count]
    return {
        template.room_id: Room(
            room_id=template.room_id,
            name=template.name,
            description=template.description,
        )
        for template in selected_templates
    }


def _connect_main_path(rooms: dict[str, Room]) -> None:
    path_ids = [room_id for room_id in MAIN_PATH_IDS if room_id in rooms]
    directions = ["north", "east", "north", "east"]
    opposites = {"north": "south", "south": "north", "east": "west", "west": "east"}
    for index, room_id in enumerate(path_ids[:-1]):
        next_room_id = path_ids[index + 1]
        direction = directions[index]
        _connect(rooms, room_id, next_room_id, direction, opposites[direction])


def _connect_side_rooms(rooms: dict[str, Room], rng: Random) -> None:
    side_ids = [room_id for room_id in rooms if room_id not in MAIN_PATH_IDS]
    anchors = [room_id for room_id in MAIN_PATH_IDS[:-1] if room_id in rooms]
    for side_id in side_ids:
        rng.shuffle(anchors)
        connected = False
        for anchor_id in anchors:
            direction_pair = _find_open_direction_pair(rooms[anchor_id], rooms[side_id], rng)
            if direction_pair is None:
                continue
            direction, opposite = direction_pair
            _connect(rooms, anchor_id, side_id, direction, opposite)
            connected = True
            break
        if not connected:
            _connect(rooms, anchors[0], side_id, "west", "east")


def _find_open_direction_pair(
    first: Room,
    second: Room,
    rng: Random,
) -> tuple[str, str] | None:
    pairs = list(DIRECTION_PAIRS)
    rng.shuffle(pairs)
    for direction, opposite in pairs:
        if direction not in first.exits and opposite not in second.exits:
            return direction, opposite
    return None


def _connect(
    rooms: dict[str, Room],
    first_id: str,
    second_id: str,
    direction: str,
    opposite: str,
) -> None:
    rooms[first_id].exits[direction] = second_id
    rooms[second_id].exits[opposite] = first_id


def _place_content(rooms: dict[str, Room], rng: Random, difficulty: str) -> None:
    config = _get_config(difficulty)
    for room_id, room in rooms.items():
        if room_id in {"gatehouse", "redoubt"}:
            continue
        if rng.random() < config.monster_chance:
            room.monster = _scaled_monster(rng.choice(MONSTER_TEMPLATES), rng, difficulty)
        if rng.random() < config.item_chance:
            room.items.append(deepcopy(rng.choice(ITEM_TEMPLATES)))
    boss = deepcopy(BOSS_TEMPLATE)
    boss.max_hp = rng.randint(*config.boss_hp_range)
    boss.hp = boss.max_hp
    rooms["redoubt"].monster = boss


def _scaled_monster(template: Monster, rng: Random, difficulty: str) -> Monster:
    config = _get_config(difficulty)
    monster = deepcopy(template)
    monster.max_hp = rng.randint(*config.monster_hp_range)
    monster.hp = monster.max_hp
    return monster
```

- [ ] **Step 4: Fix `_get_config` typing if mypy complains**

If mypy later reports `_get_config` as untyped, replace the function with:

```python
from ashen_keep.models import DifficultyConfig


def _get_config(difficulty: str) -> DifficultyConfig:
    if difficulty not in DIFFICULTIES:
        known = ", ".join(sorted(DIFFICULTIES))
        raise ValueError(f"Unknown difficulty {difficulty!r}. Expected one of: {known}.")
    return DIFFICULTIES[difficulty]
```

Also add `DifficultyConfig` to the existing `from ashen_keep.models import ...` import list.

- [ ] **Step 5: Run generation tests**

Run:

```bash
python -m pytest tests/test_generation.py -v
```

Expected: 4 passed.

- [ ] **Step 6: Run ruff**

Run:

```bash
python -m ruff check src/ashen_keep/generation.py tests/test_generation.py
```

Expected: all checks passed. If ruff flags import sorting, run:

```bash
python -m ruff check src/ashen_keep/generation.py tests/test_generation.py --fix
```

Then rerun the check.

- [ ] **Step 7: Commit**

Run:

```bash
git add src/ashen_keep/generation.py tests/test_generation.py
git commit -m "feat: generate seeded dungeons"
```

---

### Task 5: Combat actions

**Files:**
- Create: `src/ashen_keep/combat.py`
- Create: `tests/test_combat.py`

- [ ] **Step 1: Write failing combat tests**

Create `tests/test_combat.py`:

```python
from random import Random

from ashen_keep.combat import attack, defend, use_potion
from ashen_keep.models import GameStatus, Monster, Player


def test_attack_damages_monster_and_triggers_counterattack() -> None:
    player = Player(max_hp=30, hp=30, attack=6, defense=1, potions=1)
    monster = Monster(name="Hungry Goblin", max_hp=7, hp=7, attack=3, defense=0)

    result = attack(player, monster, Random(1))

    assert monster.hp < 7
    assert player.hp < 30
    assert result.status is GameStatus.IN_PROGRESS
    assert "strike" in result.message.lower()


def test_attack_defeats_monster_without_counterattack() -> None:
    player = Player(max_hp=30, hp=30, attack=10, defense=1, potions=1)
    monster = Monster(name="Ledger Imp", max_hp=4, hp=4, attack=3, defense=0)

    result = attack(player, monster, Random(1))

    assert monster.hp <= 0
    assert player.hp == 30
    assert "defeat" in result.message.lower()


def test_defend_reduces_incoming_damage() -> None:
    normal_player = Player(max_hp=30, hp=30, attack=6, defense=1, potions=1)
    defended_player = Player(max_hp=30, hp=30, attack=6, defense=1, potions=1)
    monster = Monster(name="Rust Knight", max_hp=12, hp=12, attack=6, defense=1)

    attack(normal_player, monster, Random(2))
    defend(defended_player, monster, Random(2))

    assert defended_player.hp > normal_player.hp


def test_use_potion_heals_and_consumes_potion() -> None:
    player = Player(max_hp=32, hp=10, attack=6, defense=1, potions=2)
    monster = Monster(name="Ledger Imp", max_hp=6, hp=6, attack=2, defense=1)

    result = use_potion(player, monster, Random(3), heal_amount=8)

    assert player.potions == 1
    assert player.hp >= 16
    assert "potion" in result.message.lower() or "flask" in result.message.lower()


def test_use_potion_without_potions_returns_message() -> None:
    player = Player(max_hp=32, hp=10, attack=6, defense=1, potions=0)
    monster = Monster(name="Ledger Imp", max_hp=6, hp=6, attack=2, defense=1)

    result = use_potion(player, monster, Random(3), heal_amount=8)

    assert player.potions == 0
    assert player.hp == 10
    assert "no potions" in result.message.lower()
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/test_combat.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'ashen_keep.combat'`.

- [ ] **Step 3: Implement `combat.py`**

Create `src/ashen_keep/combat.py`:

```python
"""Turn-based combat actions for Ashen Keep."""

from __future__ import annotations

from random import Random

from ashen_keep.models import ActionResult, GameStatus, Monster, Player

DEFEND_BONUS = 3


def attack(player: Player, monster: Monster, rng: Random) -> ActionResult:
    """Resolve a player attack followed by a monster counterattack if alive."""
    player_damage = _damage(player.attack, monster.defense, rng)
    monster.hp -= player_damage
    if not monster.is_alive:
        return ActionResult(
            message=f"You strike {monster.name} for {player_damage} damage and defeat it."
        )
    monster_damage = _monster_damage(monster, player, rng, defense_bonus=0)
    return _after_monster_damage(
        player,
        f"You strike {monster.name} for {player_damage} damage. "
        f"{monster.name} hits you for {monster_damage} damage.",
    )


def defend(player: Player, monster: Monster, rng: Random) -> ActionResult:
    """Resolve a defensive turn that reduces incoming monster damage."""
    monster_damage = _monster_damage(monster, player, rng, defense_bonus=DEFEND_BONUS)
    return _after_monster_damage(
        player,
        f"You raise your guard. {monster.name} hits you for {monster_damage} damage.",
    )


def use_potion(
    player: Player,
    monster: Monster,
    rng: Random,
    heal_amount: int,
) -> ActionResult:
    """Use one potion, then resolve monster counterattack if needed."""
    if player.potions <= 0:
        return ActionResult(message="You have no potions left.")
    player.potions -= 1
    healed = player.heal(heal_amount)
    monster_damage = _monster_damage(monster, player, rng, defense_bonus=0)
    return _after_monster_damage(
        player,
        f"You drink a potion and recover {healed} HP. "
        f"{monster.name} hits you for {monster_damage} damage.",
    )


def _damage(attack_value: int, defense_value: int, rng: Random) -> int:
    random_bonus = rng.randint(0, 2)
    return max(1, attack_value + random_bonus - defense_value)


def _monster_damage(
    monster: Monster,
    player: Player,
    rng: Random,
    defense_bonus: int,
) -> int:
    damage = _damage(monster.attack, player.defense + defense_bonus, rng)
    player.hp -= damage
    return damage


def _after_monster_damage(player: Player, message: str) -> ActionResult:
    if player.is_alive:
        return ActionResult(message=message)
    return ActionResult(message=f"{message} You fall.", status=GameStatus.LOST)
```

- [ ] **Step 4: Run combat tests**

Run:

```bash
python -m pytest tests/test_combat.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Run ruff**

Run:

```bash
python -m ruff check src/ashen_keep/combat.py tests/test_combat.py
```

Expected: all checks passed.

- [ ] **Step 6: Commit**

Run:

```bash
git add src/ashen_keep/combat.py tests/test_combat.py
git commit -m "feat: add combat actions"
```

---

### Task 6: Engine movement, items, and win/loss state

**Files:**
- Create: `src/ashen_keep/engine.py`
- Create: `tests/test_engine.py`
- Create: `tests/test_items.py`

- [ ] **Step 1: Write failing engine tests**

Create `tests/test_engine.py`:

```python
from ashen_keep.engine import (
    get_available_commands,
    move,
    perform_combat_action,
    start_game,
)
from ashen_keep.models import GameStatus, Monster


def test_start_game_returns_gatehouse_state() -> None:
    state = start_game(seed=7)

    assert state.current_room_id == "gatehouse"
    assert state.current_room.visited
    assert state.status is GameStatus.IN_PROGRESS


def test_move_rejects_invalid_exit() -> None:
    state = start_game(seed=7)

    result = move(state, "down")

    assert state.current_room_id == "gatehouse"
    assert "no exit" in result.message.lower()


def test_move_changes_room_and_marks_visited() -> None:
    state = start_game(seed=7)
    direction = next(iter(state.current_room.exits))
    target = state.current_room.exits[direction]

    result = move(state, direction)

    assert state.current_room_id == target
    assert state.current_room.visited
    assert target in result.message


def test_living_monster_blocks_movement() -> None:
    state = start_game(seed=7)
    state.current_room.monster = Monster("Test Guard", max_hp=5, hp=5, attack=1, defense=0)
    direction = next(iter(state.current_room.exits))

    result = move(state, direction)

    assert state.current_room_id == "gatehouse"
    assert "blocks" in result.message.lower()


def test_available_commands_include_combat_when_monster_present() -> None:
    state = start_game(seed=7)
    state.current_room.monster = Monster("Test Guard", max_hp=5, hp=5, attack=1, defense=0)

    commands = get_available_commands(state)

    assert "attack" in commands
    assert "defend" in commands
    assert "potion" in commands


def test_defeating_boss_wins_game() -> None:
    state = start_game(seed=7)
    state.current_room_id = state.boss_room_id
    boss = state.current_room.monster
    assert boss is not None
    boss.hp = 1
    state.player.attack = 99

    result = perform_combat_action(state, "attack")

    assert result.status is GameStatus.WON
    assert state.status is GameStatus.WON
```

- [ ] **Step 2: Write failing item tests**

Create `tests/test_items.py`:

```python
from ashen_keep.engine import start_game, take_item
from ashen_keep.models import Item, ItemKind


def test_take_potion_increases_potion_count() -> None:
    state = start_game(seed=7)
    state.current_room.items = [Item("Ration Flask", kind=ItemKind.POTION, heal_amount=8)]
    before = state.player.potions

    result = take_item(state)

    assert state.player.potions == before + 1
    assert state.current_room.items == []
    assert "ration flask" in result.message.lower()


def test_take_better_weapon_updates_attack_and_name() -> None:
    state = start_game(seed=7)
    state.current_room.items = [Item("Iron Sword", kind=ItemKind.WEAPON, bonus=2)]
    before = state.player.attack

    result = take_item(state)

    assert state.player.attack == before + 2
    assert state.player.weapon_name == "Iron Sword"
    assert "equip" in result.message.lower()


def test_take_weaker_weapon_does_not_reduce_attack() -> None:
    state = start_game(seed=7)
    state.player.attack = 10
    state.player.weapon_name = "Quartermaster's Sabre"
    state.current_room.items = [Item("Iron Sword", kind=ItemKind.WEAPON, bonus=2)]

    result = take_item(state)

    assert state.player.attack == 10
    assert state.player.weapon_name == "Quartermaster's Sabre"
    assert "leave" in result.message.lower()


def test_take_better_armor_updates_defense_and_name() -> None:
    state = start_game(seed=7)
    state.current_room.items = [Item("Stamped Buckler", kind=ItemKind.ARMOR, bonus=2)]
    before = state.player.defense

    take_item(state)

    assert state.player.defense == before + 2
    assert state.player.armor_name == "Stamped Buckler"


def test_take_without_items_returns_message() -> None:
    state = start_game(seed=7)
    state.current_room.items = []

    result = take_item(state)

    assert "nothing" in result.message.lower()
```

- [ ] **Step 3: Run tests to verify failure**

Run:

```bash
python -m pytest tests/test_engine.py tests/test_items.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'ashen_keep.engine'`.

- [ ] **Step 4: Implement `engine.py`**

Create `src/ashen_keep/engine.py`:

```python
"""Public game engine API for Ashen Keep."""

from __future__ import annotations

from random import Random

from ashen_keep.combat import attack, defend, use_potion
from ashen_keep.content import DIFFICULTIES, VICTORY_TEXT
from ashen_keep.generation import create_dungeon
from ashen_keep.models import ActionResult, GameState, GameStatus, Item, ItemKind

DIRECTION_ALIASES = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
}


def start_game(seed: int | None = None, difficulty: str = "easy") -> GameState:
    """Start a new game."""
    return create_dungeon(seed=seed, difficulty=difficulty)


def move(state: GameState, direction: str) -> ActionResult:
    """Move the player through an exit if possible."""
    if state.status is not GameStatus.IN_PROGRESS:
        return ActionResult("The game is already over.", status=state.status)
    if state.current_room.has_living_monster:
        return ActionResult(f"{state.current_room.monster.name} blocks your path.")
    normalized = DIRECTION_ALIASES.get(direction.lower(), direction.lower())
    if normalized not in state.current_room.exits:
        exits = ", ".join(sorted(state.current_room.exits)) or "none"
        return ActionResult(f"There is no exit {normalized}. Available exits: {exits}.")
    next_room_id = state.current_room.exits[normalized]
    state.current_room_id = next_room_id
    state.current_room.visited = True
    return ActionResult(f"You move {normalized} to {next_room_id}.")


def take_item(state: GameState) -> ActionResult:
    """Take the first item in the current room and apply its effect."""
    if state.status is not GameStatus.IN_PROGRESS:
        return ActionResult("The game is already over.", status=state.status)
    if not state.current_room.items:
        return ActionResult("There is nothing useful to take.")
    item = state.current_room.items.pop(0)
    return _apply_item(state, item)


def perform_combat_action(state: GameState, action: str) -> ActionResult:
    """Perform one combat action against the current room's monster."""
    if state.status is not GameStatus.IN_PROGRESS:
        return ActionResult("The game is already over.", status=state.status)
    monster = state.current_room.monster
    if monster is None or not monster.is_alive:
        return ActionResult("There is nothing here to fight.")
    rng = Random(state.seed)
    normalized = action.lower()
    if normalized == "attack":
        result = attack(state.player, monster, rng)
    elif normalized == "defend":
        result = defend(state.player, monster, rng)
    elif normalized == "potion":
        heal_amount = DIFFICULTIES[state.difficulty].potion_heal
        result = use_potion(state.player, monster, rng, heal_amount)
    else:
        return ActionResult(f"Unknown combat action: {action}.")
    if result.status is GameStatus.LOST:
        state.status = GameStatus.LOST
        return result
    if monster.is_boss and not monster.is_alive:
        state.status = GameStatus.WON
        return ActionResult(VICTORY_TEXT, status=GameStatus.WON)
    return result


def get_available_commands(state: GameState) -> list[str]:
    """Return commands that make sense in the current state."""
    if state.status is not GameStatus.IN_PROGRESS:
        return ["quit"]
    commands = ["look", "status", "help", "quit"]
    if state.current_room.has_living_monster:
        commands.extend(["attack", "defend", "potion"])
    else:
        commands.extend([f"move {direction}" for direction in sorted(state.current_room.exits)])
        if state.current_room.items:
            commands.append("take")
    return commands


def _apply_item(state: GameState, item: Item) -> ActionResult:
    if item.kind is ItemKind.POTION:
        state.player.potions += 1
        return ActionResult(f"You take {item.name}. Potion count is now {state.player.potions}.")
    if item.kind is ItemKind.WEAPON:
        base_attack = DIFFICULTIES[state.difficulty].player_attack
        current_bonus = state.player.attack - base_attack
        if item.bonus > current_bonus:
            state.player.attack = base_attack + item.bonus
            state.player.weapon_name = item.name
            return ActionResult(f"You equip {item.name}. Attack is now {state.player.attack}.")
        return ActionResult(f"You leave {item.name}; your current weapon is better.")
    if item.kind is ItemKind.ARMOR:
        base_defense = DIFFICULTIES[state.difficulty].player_defense
        current_bonus = state.player.defense - base_defense
        if item.bonus > current_bonus:
            state.player.defense = base_defense + item.bonus
            state.player.armor_name = item.name
            return ActionResult(f"You equip {item.name}. Defense is now {state.player.defense}.")
        return ActionResult(f"You leave {item.name}; your current armor is better.")
    return ActionResult(f"You cannot use {item.name}.")
```

- [ ] **Step 5: Run engine and item tests**

Run:

```bash
python -m pytest tests/test_engine.py tests/test_items.py -v
```

Expected: all tests pass.

- [ ] **Step 6: Run ruff**

Run:

```bash
python -m ruff check src/ashen_keep/engine.py tests/test_engine.py tests/test_items.py
```

Expected: all checks passed.

- [ ] **Step 7: Commit**

Run:

```bash
git add src/ashen_keep/engine.py tests/test_engine.py tests/test_items.py
git commit -m "feat: add game engine actions"
```

---

### Task 7: Rendering and CLI

**Files:**
- Create: `src/ashen_keep/rendering.py`
- Create: `src/ashen_keep/cli.py`
- Create: `src/ashen_keep/__main__.py`
- Create: `tests/test_cli_smoke.py`

- [ ] **Step 1: Write failing CLI smoke tests**

Create `tests/test_cli_smoke.py`:

```python
import subprocess
import sys

from ashen_keep.engine import start_game
from ashen_keep.rendering import render_room, render_status


def test_render_room_includes_room_name_and_exits() -> None:
    state = start_game(seed=7)

    rendered = render_room(state)

    assert state.current_room.name in rendered
    assert "Exits:" in rendered


def test_render_status_includes_hp_and_equipment() -> None:
    state = start_game(seed=7)

    rendered = render_status(state)

    assert "HP" in rendered
    assert state.player.weapon_name in rendered
    assert state.player.armor_name in rendered


def test_module_help_runs() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ashen_keep", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "Ashen Keep" in completed.stdout
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/test_cli_smoke.py -v
```

Expected: FAIL with missing `rendering` or `__main__` module.

- [ ] **Step 3: Implement `rendering.py`**

Create `src/ashen_keep/rendering.py`:

```python
"""Text rendering helpers for the Ashen Keep CLI."""

from __future__ import annotations

from ashen_keep.models import ActionResult, GameState


def render_room(state: GameState) -> str:
    """Render the player's current room."""
    room = state.current_room
    lines = [room.name, "-" * len(room.name), room.description]
    if room.has_living_monster and room.monster is not None:
        lines.append(f"Monster: {room.monster.name} ({room.monster.hp} HP)")
    if room.items:
        lines.append("Items: " + ", ".join(item.name for item in room.items))
    exits = ", ".join(sorted(room.exits)) or "none"
    lines.append(f"Exits: {exits}")
    return "\n".join(lines)


def render_status(state: GameState) -> str:
    """Render player status."""
    player = state.player
    return (
        f"HP: {player.hp}/{player.max_hp}\n"
        f"Attack: {player.attack} ({player.weapon_name})\n"
        f"Defense: {player.defense} ({player.armor_name})\n"
        f"Potions: {player.potions}"
    )


def render_result(result: ActionResult) -> str:
    """Render an action result."""
    return result.message
```

- [ ] **Step 4: Implement `cli.py`**

Create `src/ashen_keep/cli.py`:

```python
"""Command-line interface for Ashen Keep."""

from __future__ import annotations

import argparse

from ashen_keep.content import TITLE_ART
from ashen_keep.engine import (
    get_available_commands,
    move,
    perform_combat_action,
    start_game,
    take_item,
)
from ashen_keep.models import GameStatus
from ashen_keep.rendering import render_result, render_room, render_status

HELP_TEXT = """Commands:
  look                 Show the current room again
  status               Show HP, equipment, and potions
  move <direction>     Move north, east, south, or west
  n/e/s/w              Short movement commands
  take                 Take the first item in the room
  attack               Attack the current monster
  defend               Guard against the current monster
  potion               Drink a healing potion
  help                 Show this help text
  quit                 Leave the game
""".strip()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Ashen Keep roguelike-lite CLI")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducible dungeons")
    parser.add_argument("--difficulty", default="easy", help="Difficulty name; default: easy")
    parser.add_argument("--demo", action="store_true", help="Use a friendly demo seed")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the Ashen Keep CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    seed = 7 if args.demo and args.seed is None else args.seed
    state = start_game(seed=seed, difficulty=args.difficulty)
    print(TITLE_ART)
    print()
    print(render_room(state))
    print()
    print("Type 'help' for commands.")
    while state.status is GameStatus.IN_PROGRESS:
        command = input("> ").strip().lower()
        if not command:
            continue
        if command == "quit":
            state.status = GameStatus.QUIT
            print("You leave Slop Keep for another day.")
            break
        output = handle_command(state, command)
        print(output)
    return 0


def handle_command(state, command: str) -> str:  # type: ignore[no-untyped-def]
    """Handle one CLI command and return text to print."""
    if command == "help":
        return HELP_TEXT
    if command == "look":
        return render_room(state)
    if command == "status":
        return render_status(state)
    if command == "commands":
        return "Available: " + ", ".join(get_available_commands(state))
    if command == "take":
        return render_result(take_item(state))
    if command in {"attack", "defend", "potion"}:
        result = perform_combat_action(state, command)
        return render_result(result)
    if command in {"n", "s", "e", "w"}:
        return render_result(move(state, command))
    if command.startswith("move "):
        return render_result(move(state, command.removeprefix("move ").strip()))
    return "Unknown command. Type 'help' for commands."


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Implement `__main__.py`**

Create `src/ashen_keep/__main__.py`:

```python
"""Entry point for `python -m ashen_keep`."""

from ashen_keep.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Fix CLI typing before mypy**

Replace the untyped `handle_command` function in `src/ashen_keep/cli.py` with:

```python
from ashen_keep.models import GameState, GameStatus
```

Then use this exact function signature and body:

```python
def handle_command(state: GameState, command: str) -> str:
    """Handle one CLI command and return text to print."""
    if command == "help":
        return HELP_TEXT
    if command == "look":
        return render_room(state)
    if command == "status":
        return render_status(state)
    if command == "commands":
        return "Available: " + ", ".join(get_available_commands(state))
    if command == "take":
        return render_result(take_item(state))
    if command in {"attack", "defend", "potion"}:
        result = perform_combat_action(state, command)
        return render_result(result)
    if command in {"n", "s", "e", "w"}:
        return render_result(move(state, command))
    if command.startswith("move "):
        return render_result(move(state, command.removeprefix("move ").strip()))
    return "Unknown command. Type 'help' for commands."
```

- [ ] **Step 7: Run CLI smoke tests**

Run:

```bash
python -m pytest tests/test_cli_smoke.py -v
```

Expected: 3 passed.

- [ ] **Step 8: Run module help manually**

Run:

```bash
python -m ashen_keep --help
```

Expected: output includes `Ashen Keep roguelike-lite CLI`, `--seed`, and `--demo`.

- [ ] **Step 9: Run ruff**

Run:

```bash
python -m ruff check src/ashen_keep/rendering.py src/ashen_keep/cli.py src/ashen_keep/__main__.py tests/test_cli_smoke.py
```

Expected: all checks passed.

- [ ] **Step 10: Commit**

Run:

```bash
git add src/ashen_keep/rendering.py src/ashen_keep/cli.py src/ashen_keep/__main__.py tests/test_cli_smoke.py
git commit -m "feat: add command line interface"
```

---

### Task 8: Documentation and AI usage records

**Files:**
- Create: `README.md`
- Create: `docs/DESIGN.md`
- Create: `docs/AI_USAGE.md`

- [ ] **Step 1: Create `README.md`**

Write:

```markdown
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
```

- [ ] **Step 2: Create `docs/DESIGN.md`**

Write:

```markdown
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
```

- [ ] **Step 3: Create `docs/AI_USAGE.md`**

Write:

```markdown
# Generative AI Usage

This project used generative AI tools. The student reviewed the outputs and remains responsible for the submitted work.

## Tools used

- ChatGPT / pi coding agent conversation.

## How AI was used

AI was used to:

- brainstorm project ideas from the course prompt,
- compare possible scopes for a solo final project,
- design the Ashen Keep architecture,
- draft an implementation plan,
- draft Python source code,
- draft tests,
- draft documentation,
- generate small amounts of text flavor and ASCII title art.

## What AI produced

AI produced drafts of:

- the project design spec,
- the implementation plan,
- module structure suggestions,
- game content names and descriptions,
- Python implementation code,
- pytest tests,
- README content,
- this AI usage documentation.

## Human review and edits

The student selected the final project direction, approved the scope, chose the boss victory condition, selected the easy-by-default design, chose the project name, and reviewed generated plans and code before submission. The student ran tests and style checks locally and used Git/GitHub workflow practices for the final submission.

## Limitations

AI-generated code and text can contain mistakes. The project relies on automated tests, Ruff, mypy, manual review, and manual gameplay checks to catch issues before submission.
```

- [ ] **Step 4: Run documentation spell/sanity check manually**

Run:

```bash
python - <<'PY'
from pathlib import Path
for path in [Path('README.md'), Path('docs/DESIGN.md'), Path('docs/AI_USAGE.md')]:
    text = path.read_text()
    unfinished_markers = ("T" + "BD", "TO" + "DO")
    for marker in unfinished_markers:
        assert marker not in text
    print(path, 'ok')
PY
```

Expected:

```text
README.md ok
docs/DESIGN.md ok
docs/AI_USAGE.md ok
```

- [ ] **Step 5: Commit**

Run:

```bash
git add README.md docs/DESIGN.md docs/AI_USAGE.md
git commit -m "docs: add user and AI usage documentation"
```

---

### Task 9: Full verification and polish

**Files:**
- Modify only files needed to fix verification failures.

- [ ] **Step 1: Run the full test suite**

Run:

```bash
python -m pytest -v
```

Expected: all tests pass.

- [ ] **Step 2: Run Ruff check**

Run:

```bash
python -m ruff check src tests
```

Expected: all checks passed.

- [ ] **Step 3: Run Ruff format check**

Run:

```bash
python -m ruff format --check src tests
```

Expected: all files already formatted. If it fails, run:

```bash
python -m ruff format src tests
python -m ruff format --check src tests
```

- [ ] **Step 4: Run mypy**

Run:

```bash
python -m mypy src tests
```

Expected: success with no issues. If mypy finds missing annotations, add exact type annotations rather than weakening mypy settings.

- [ ] **Step 5: Run CLI help**

Run:

```bash
python -m ashen_keep --help
```

Expected: help output exits with status 0 and lists `--seed`, `--difficulty`, and `--demo`.

- [ ] **Step 6: Run a short manual demo smoke path**

Run:

```bash
python -m ashen_keep --demo
```

At the prompt, try:

```text
status
look
commands
quit
```

Expected: no crash; status and room text are readable.

- [ ] **Step 7: Commit verification fixes if any**

If any files changed during verification, run:

```bash
git status --short
git add <changed-files>
git commit -m "fix: polish verified game build"
```

If no files changed, do not create an empty commit.

---

### Task 10: GitHub repository setup and project plan issues

**Files:**
- No code files required.

- [ ] **Step 1: Create the GitHub repository**

Create a public or private GitHub repository named `ashen-keep`.

Suggested GitHub description:

```text
A small Python roguelike-lite library and CLI for exploring Slop Keep.
```

- [ ] **Step 2: Push local repository**

Run, replacing `YOUR-USERNAME` with the GitHub account:

```bash
git remote add origin git@github.com:YOUR-USERNAME/ashen-keep.git
git branch -M main
git push -u origin main
```

Expected: repository is visible on GitHub with README, source, tests, and docs.

- [ ] **Step 3: Create GitHub issues**

Create these issues from the GitHub UI or `gh issue create`:

```text
Title: Set up Python package and developer tooling
Body: Configure package metadata, pytest, Ruff, mypy, and initial README structure.
Assignee: Leo Liang
```

```text
Title: Implement core game models
Body: Add Player, Monster, Item, Room, GameState, DifficultyConfig, and ActionResult models with tests.
Assignee: Leo Liang
```

```text
Title: Implement seeded dungeon generation
Body: Generate a small branching dungeon with a reachable boss room, easy default balance, and reproducible seeds.
Assignee: Leo Liang
```

```text
Title: Implement combat and item rules
Body: Add attack, defend, potion, item pickup, automatic equipment upgrades, and related tests.
Assignee: Leo Liang
```

```text
Title: Implement engine API and CLI
Body: Expose start_game, move, take_item, perform_combat_action, rendering, and a thin command-line loop.
Assignee: Leo Liang
```

```text
Title: Add tests and verification documentation
Body: Cover generation, combat, movement, items, win/loss states, and CLI smoke behavior. Document how to run tests and checks.
Assignee: Leo Liang
```

```text
Title: Document architecture and generative AI usage
Body: Write architecture documentation and an exhaustive record of AI tools, usage, outputs, and human review.
Assignee: Leo Liang
```

- [ ] **Step 4: Final Canvas submission note**

Prepare this Canvas submission text:

```text
Repository: https://github.com/YOUR-USERNAME/ashen-keep
Group members: Leo Liang
Project: Ashen Keep, a Python roguelike-lite library and CLI.
```

---

## Self-Review

Spec coverage:

- Library/CLI split: Tasks 2, 4, 5, 6, and 7.
- Easy-by-default roguelike-lite: Tasks 3 and 4.
- Boss victory condition: Tasks 4 and 6.
- Attack/defend/potion combat: Task 5.
- Potions and simple equipment: Task 6.
- Small branching graph: Task 4.
- Seed reproducibility: Task 4.
- ASCII/text flavor: Tasks 3 and 7.
- Tests: Tasks 1 through 9.
- Ruff/mypy/pytest docs: Tasks 1, 8, and 9.
- AI usage documentation: Task 8.
- GitHub issues/project plan: Task 10.

Placeholder scan: no unfinished markers or incomplete implementation placeholders are intentionally left in this plan.

Type consistency: public types and function names match the proposed files: `Player`, `Monster`, `Item`, `Room`, `GameState`, `ActionResult`, `start_game`, `move`, `take_item`, `perform_combat_action`, `render_room`, and `render_status`.
