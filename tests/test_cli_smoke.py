import subprocess
import sys

from ashen_keep.engine import start_game
from ashen_keep.rendering import render_room, render_status


def test_render_room_includes_room_name_and_exits() -> None:
    state = start_game(seed=7)

    rendered = render_room(state)

    assert state.current_room.name in rendered
    assert "Exits:" in rendered


def test_render_status_includes_hp_and_equipment() -> None:
    state = start_game(seed=7)

    rendered = render_status(state)

    assert "HP" in rendered
    assert state.player.weapon_name in rendered
    assert state.player.armor_name in rendered


def test_module_help_runs() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ashen_keep", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "Ashen Keep" in completed.stdout
