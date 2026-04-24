from ashen_keep.engine import start_game, take_item
from ashen_keep.models import Item, ItemKind


def test_take_potion_increases_potion_count() -> None:
    state = start_game(seed=7)
    state.current_room.items = [
        Item("Ration Flask", kind=ItemKind.POTION, heal_amount=8)
    ]
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
