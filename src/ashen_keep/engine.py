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
        monster = state.current_room.monster
        assert monster is not None
        return ActionResult(f"{monster.name} blocks your path.")
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


def drink_potion(state: GameState) -> ActionResult:
    """Drink a potion outside combat without triggering a monster attack."""
    if state.status is not GameStatus.IN_PROGRESS:
        return ActionResult("The game is already over.", status=state.status)
    if state.player.potions <= 0:
        return ActionResult("You have no potions left.")
    if state.player.hp >= state.player.max_hp:
        return ActionResult("You are already at full HP.")
    state.player.potions -= 1
    heal_amount = DIFFICULTIES[state.difficulty].potion_heal
    healed = state.player.heal(heal_amount)
    return ActionResult(
        f"You drink a potion and recover {healed} HP. "
        f"Potions left: {state.player.potions}."
    )


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
    if state.player.potions > 0 and state.player.hp < state.player.max_hp:
        commands.append("potion")
    if state.current_room.has_living_monster:
        commands.extend(["attack", "defend"])
        if "potion" not in commands and state.player.potions > 0:
            commands.append("potion")
    else:
        commands.extend(
            [f"move {direction}" for direction in sorted(state.current_room.exits)]
        )
        if state.current_room.items:
            commands.append("take")
    return commands


def _apply_item(state: GameState, item: Item) -> ActionResult:
    if item.kind is ItemKind.POTION:
        state.player.potions += 1
        return ActionResult(
            f"You take {item.name}. Potion count is now {state.player.potions}."
        )
    if item.kind is ItemKind.WEAPON:
        base_attack = DIFFICULTIES[state.difficulty].player_attack
        current_bonus = state.player.attack - base_attack
        if item.bonus > current_bonus:
            state.player.attack = base_attack + item.bonus
            state.player.weapon_name = item.name
            return ActionResult(
                f"You equip {item.name}. Attack is now {state.player.attack}."
            )
        return ActionResult(f"You leave {item.name}; your current weapon is better.")
    if item.kind is ItemKind.ARMOR:
        base_defense = DIFFICULTIES[state.difficulty].player_defense
        current_bonus = state.player.defense - base_defense
        if item.bonus > current_bonus:
            state.player.defense = base_defense + item.bonus
            state.player.armor_name = item.name
            return ActionResult(
                f"You equip {item.name}. Defense is now {state.player.defense}."
            )
        return ActionResult(f"You leave {item.name}; your current armor is better.")
    return ActionResult(f"You cannot use {item.name}.")
