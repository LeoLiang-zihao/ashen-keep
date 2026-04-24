from collections import deque

import pytest

from ashen_keep.generation import create_dungeon, create_player
from ashen_keep.models import GameStatus


def boss_is_reachable(
    state_room_ids: dict[str, list[str]], start: str, boss: str
) -> bool:
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
    boss = state.rooms[state.boss_room_id].monster
    assert boss is not None
    assert boss.is_boss


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
    with pytest.raises(ValueError, match="Unknown difficulty"):
        create_dungeon(seed=1, difficulty="nightmare")
