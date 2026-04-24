from ashen_keep.content import (
    BOSS_TEMPLATE,
    DIFFICULTIES,
    ITEM_TEMPLATES,
    MONSTER_TEMPLATES,
    ROOM_TEMPLATES,
    TITLE_ART,
)
from ashen_keep.models import ItemKind


def test_easy_difficulty_is_default_friendly() -> None:
    easy = DIFFICULTIES["easy"]

    assert easy.room_count == 9
    assert easy.player_hp >= 30
    assert easy.starting_potions >= 2
    assert easy.potion_heal == 8


def test_content_has_enough_room_templates() -> None:
    assert len(ROOM_TEMPLATES) >= 9
    assert ROOM_TEMPLATES[0].room_id == "gatehouse"


def test_content_has_monsters_items_and_boss() -> None:
    assert len(MONSTER_TEMPLATES) >= 4
    assert len(ITEM_TEMPLATES) >= 4
    assert BOSS_TEMPLATE.is_boss
    assert any(item.kind is ItemKind.POTION for item in ITEM_TEMPLATES)
    assert any(item.kind is ItemKind.WEAPON for item in ITEM_TEMPLATES)
    assert any(item.kind is ItemKind.ARMOR for item in ITEM_TEMPLATES)


def test_title_art_names_game() -> None:
    assert "ASHEN KEEP" in TITLE_ART
