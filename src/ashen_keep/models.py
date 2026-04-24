"""Core domain models for Ashen Keep."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class GameStatus(StrEnum):
    """Overall lifecycle status for a game."""

    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"
    QUIT = "quit"


class ItemKind(StrEnum):
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
