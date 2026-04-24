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
            message=(
                f"You strike {monster.name} for {player_damage} damage "
                "and defeat it."
            )
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
