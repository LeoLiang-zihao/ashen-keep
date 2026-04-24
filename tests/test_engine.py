from ashen_keep.engine import (
    drink_potion,
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
    state.current_room.monster = Monster(
        "Test Guard", max_hp=5, hp=5, attack=1, defense=0
    )
    direction = next(iter(state.current_room.exits))

    result = move(state, direction)

    assert state.current_room_id == "gatehouse"
    assert "blocks" in result.message.lower()


def test_available_commands_include_combat_when_monster_present() -> None:
    state = start_game(seed=7)
    state.current_room.monster = Monster(
        "Test Guard", max_hp=5, hp=5, attack=1, defense=0
    )

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


def test_drink_potion_outside_combat_heals_without_fighting() -> None:
    state = start_game(seed=7)
    state.player.hp = 20
    before_potions = state.player.potions

    result = drink_potion(state)

    assert state.player.hp == 28
    assert state.player.potions == before_potions - 1
    assert "recover 8 hp" in result.message.lower()


def test_drink_potion_at_full_hp_does_not_consume_potion() -> None:
    state = start_game(seed=7)
    before_potions = state.player.potions

    result = drink_potion(state)

    assert state.player.hp == state.player.max_hp
    assert state.player.potions == before_potions
    assert "already at full hp" in result.message.lower()


def test_available_commands_include_potion_outside_combat_when_damaged() -> None:
    state = start_game(seed=7)
    state.player.hp = 20

    commands = get_available_commands(state)

    assert "potion" in commands
