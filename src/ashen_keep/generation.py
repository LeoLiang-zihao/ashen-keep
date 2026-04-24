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
from ashen_keep.models import DifficultyConfig, GameState, Monster, Player, Room

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
    _place_content(rooms, rng, config)
    rooms["gatehouse"].visited = True
    return GameState(
        player=create_player(difficulty),
        rooms=rooms,
        current_room_id="gatehouse",
        boss_room_id="redoubt",
        seed=seed,
        difficulty=difficulty,
    )


def _get_config(difficulty: str) -> DifficultyConfig:
    if difficulty not in DIFFICULTIES:
        known = ", ".join(sorted(DIFFICULTIES))
        raise ValueError(
            f"Unknown difficulty {difficulty!r}. Expected one of: {known}."
        )
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
        shuffled_anchors = anchors[:]
        rng.shuffle(shuffled_anchors)
        for anchor_id in shuffled_anchors:
            direction_pair = _find_open_direction_pair(
                rooms[anchor_id], rooms[side_id], rng
            )
            if direction_pair is None:
                continue
            direction, opposite = direction_pair
            _connect(rooms, anchor_id, side_id, direction, opposite)
            break


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


def _place_content(
    rooms: dict[str, Room], rng: Random, config: DifficultyConfig
) -> None:
    for room_id, room in rooms.items():
        if room_id in {"gatehouse", "redoubt"}:
            continue
        if rng.random() < config.monster_chance:
            room.monster = _scaled_monster(rng.choice(MONSTER_TEMPLATES), rng, config)
        if rng.random() < config.item_chance:
            room.items.append(deepcopy(rng.choice(ITEM_TEMPLATES)))
    boss = deepcopy(BOSS_TEMPLATE)
    boss.max_hp = rng.randint(*config.boss_hp_range)
    boss.hp = boss.max_hp
    rooms["redoubt"].monster = boss


def _scaled_monster(
    template: Monster, rng: Random, config: DifficultyConfig
) -> Monster:
    monster = deepcopy(template)
    monster.max_hp = rng.randint(*config.monster_hp_range)
    monster.hp = monster.max_hp
    return monster
