"""Command-line interface for Ashen Keep."""

from __future__ import annotations

import argparse

from ashen_keep.content import TITLE_ART
from ashen_keep.engine import (
    get_available_commands,
    move,
    perform_combat_action,
    start_game,
    take_item,
)
from ashen_keep.models import GameState, GameStatus
from ashen_keep.rendering import render_result, render_room, render_status

HELP_TEXT = """Commands:
  look                 Show the current room again
  status               Show HP, equipment, and potions
  move <direction>     Move north, east, south, or west
  n/e/s/w              Short movement commands
  take                 Take the first item in the room
  attack               Attack the current monster
  defend               Guard against the current monster
  potion               Drink a healing potion
  help                 Show this help text
  quit                 Leave the game
""".strip()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Ashen Keep roguelike-lite CLI")
    parser.add_argument(
        "--seed", type=int, default=None, help="Seed for reproducible dungeons"
    )
    parser.add_argument(
        "--difficulty", default="easy", help="Difficulty name; default: easy"
    )
    parser.add_argument("--demo", action="store_true", help="Use a friendly demo seed")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the Ashen Keep CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    seed = 7 if args.demo and args.seed is None else args.seed
    state = start_game(seed=seed, difficulty=args.difficulty)
    print(TITLE_ART)
    print()
    print(render_room(state))
    print()
    print("Type 'help' for commands.")
    while state.status is GameStatus.IN_PROGRESS:
        command = input("> ").strip().lower()
        if not command:
            continue
        if command == "quit":
            state.status = GameStatus.QUIT
            print("You leave Slop Keep for another day.")
            break
        output = handle_command(state, command)
        print(output)
    return 0


def handle_command(state: GameState, command: str) -> str:
    """Handle one CLI command and return text to print."""
    if command == "help":
        return HELP_TEXT
    if command == "look":
        return render_room(state)
    if command == "status":
        return render_status(state)
    if command == "commands":
        return "Available: " + ", ".join(get_available_commands(state))
    if command == "take":
        return render_result(take_item(state))
    if command in {"attack", "defend", "potion"}:
        result = perform_combat_action(state, command)
        return render_result(result)
    if command in {"n", "s", "e", "w"}:
        return render_result(move(state, command))
    if command.startswith("move "):
        return render_result(move(state, command.removeprefix("move ").strip()))
    return "Unknown command. Type 'help' for commands."


if __name__ == "__main__":
    raise SystemExit(main())
