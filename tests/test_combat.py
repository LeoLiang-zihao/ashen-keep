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
    first_monster = Monster(name="Rust Knight", max_hp=12, hp=12, attack=6, defense=1)
    second_monster = Monster(name="Rust Knight", max_hp=12, hp=12, attack=6, defense=1)

    attack(normal_player, first_monster, Random(2))
    defend(defended_player, second_monster, Random(2))

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
