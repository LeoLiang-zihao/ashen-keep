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
