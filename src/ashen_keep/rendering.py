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
