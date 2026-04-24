"""Static content and balance data for Ashen Keep."""

from __future__ import annotations

from dataclasses import dataclass

from ashen_keep.models import DifficultyConfig, Item, ItemKind, Monster

TITLE_ART = r"""
    _        _                 _  __
   / \   ___| |__   ___ _ __  | |/ /___  ___ _ __
  / _ \ / __| '_ \ / _ \ '_ \ | ' // _ \/ _ \ '_ \
 / ___ \\__ \ | | |  __/ | | || . \  __/  __/ |_) |
/_/   \_\___/_| |_|\___|_| |_||_|\_\___|\___| .__/
                                             |_|
                  ASHEN KEEP
""".strip("\n")

VICTORY_TEXT = "The Last Warden falls. Slop Keep exhales dust and old orders."
DEFEAT_TEXT = "Your lamp gutters out beneath the stamped stones of Slop Keep."


@dataclass(frozen=True, slots=True)
class RoomTemplate:
    """Static room content used during generation."""

    room_id: str
    name: str
    description: str


ROOM_TEMPLATES: tuple[RoomTemplate, ...] = (
    RoomTemplate(
        "gatehouse",
        "Gatehouse of Ash",
        "A cold archway opens beneath torn banners and gray stone teeth.",
    ),
    RoomTemplate(
        "ration_hall",
        "Ration Hall",
        "Long tables wait in perfect rows, each marked by a chipped tin bowl.",
    ),
    RoomTemplate(
        "stamped_archive",
        "Stamped Archive",
        "Shelves of ledgers sag under seals no living clerk remembers.",
    ),
    RoomTemplate(
        "banner_gallery",
        "Banner Gallery",
        "Faded cloth hangs like captured dusk above the cracked floor.",
    ),
    RoomTemplate(
        "quartermaster_vault",
        "Quartermaster's Vault",
        "Locked crates split open around a desk carved with tally marks.",
    ),
    RoomTemplate(
        "iron_chapel",
        "Iron Chapel",
        "Iron votive stands line the walls, each bent toward a silent altar.",
    ),
    RoomTemplate(
        "barracks",
        "Dust-Bound Barracks",
        "Neat bunks remain made for soldiers who never returned to them.",
    ),
    RoomTemplate(
        "permit_office",
        "Permit Office",
        "A brass window divides the room, though no one waits in line now.",
    ),
    RoomTemplate(
        "redoubt",
        "Redoubt of the Last Warden",
        "A final chamber of blackened stone holds a throne, a ledger, and a blade.",
    ),
)

MONSTER_TEMPLATES: tuple[Monster, ...] = (
    Monster("Hungry Goblin", max_hp=7, hp=7, attack=3, defense=0),
    Monster("Ledger Imp", max_hp=6, hp=6, attack=2, defense=1),
    Monster("Dust-Bound Guard", max_hp=10, hp=10, attack=4, defense=1),
    Monster("Banner Wraith", max_hp=9, hp=9, attack=5, defense=0),
    Monster("Rust Knight", max_hp=12, hp=12, attack=4, defense=2),
)

BOSS_TEMPLATE = Monster(
    "The Last Warden",
    max_hp=22,
    hp=22,
    attack=5,
    defense=1,
    is_boss=True,
    description="A crowned jailer of old commands, still guarding a ruined chain.",
)

ITEM_TEMPLATES: tuple[Item, ...] = (
    Item(
        "Healing Potion",
        kind=ItemKind.POTION,
        heal_amount=8,
        description="A clear draught that closes fresh wounds.",
    ),
    Item(
        "Ration Flask",
        kind=ItemKind.POTION,
        heal_amount=8,
        description="A bitter flask from the quartermaster's emergency shelf.",
    ),
    Item(
        "Iron Sword",
        kind=ItemKind.WEAPON,
        bonus=2,
        description="A plain blade with a registry number etched near the hilt.",
    ),
    Item(
        "Quartermaster's Sabre",
        kind=ItemKind.WEAPON,
        bonus=3,
        description="A curved service blade, polished by someone very afraid.",
    ),
    Item(
        "Worn Shield",
        kind=ItemKind.ARMOR,
        bonus=1,
        description="A dented shield that still knows its duty.",
    ),
    Item(
        "Stamped Buckler",
        kind=ItemKind.ARMOR,
        bonus=2,
        description="A compact shield stamped with an unreadable seal.",
    ),
)

DIFFICULTIES: dict[str, DifficultyConfig] = {
    "easy": DifficultyConfig(
        name="easy",
        room_count=9,
        monster_chance=0.45,
        item_chance=0.60,
        player_hp=32,
        player_attack=6,
        player_defense=1,
        starting_potions=2,
        monster_hp_range=(6, 12),
        boss_hp_range=(18, 24),
        potion_heal=8,
    )
}
