"""Utility helpers for the MCP Agent Mail service."""

from __future__ import annotations

import random
import re
from typing import Iterable, Optional

ADJECTIVES: Iterable[str] = (
    # Original 12
    "Red",
    "Orange",
    "Pink",
    "Black",
    "Purple",
    "Blue",
    "Brown",
    "White",
    "Green",
    "Chartreuse",
    "Lilac",
    "Fuchsia",
    # Extended colors
    "Silver",
    "Gold",
    "Crimson",
    "Amber",
    "Coral",
    "Cyan",
    "Indigo",
    "Jade",
    "Magenta",
    "Maroon",
    "Navy",
    "Olive",
    "Scarlet",
    "Teal",
    "Violet",
    "Azure",
    "Bronze",
    "Copper",
    "Ivory",
    "Pearl",
    "Ruby",
    "Sage",
    "Sand",
    "Slate",
    "Steel",
    "Sunny",
    "Rusty",
    "Misty",
    "Dusty",
    "Frosty",
)
NOUNS: Iterable[str] = (
    # Original 11
    "Stone",
    "Lake",
    "Dog",
    "Creek",
    "Pond",
    "Cat",
    "Bear",
    "Mountain",
    "Hill",
    "Snow",
    "Castle",
    # Extended nature
    "River",
    "Forest",
    "Meadow",
    "Valley",
    "Ridge",
    "Canyon",
    "Cliff",
    "Shore",
    "Island",
    "Dune",
    "Marsh",
    "Grove",
    "Glen",
    "Bluff",
    "Rapids",
    # Extended animals
    "Wolf",
    "Hawk",
    "Owl",
    "Fox",
    "Deer",
    "Elk",
    "Crow",
    "Swan",
    "Heron",
    "Finch",
    "Otter",
    "Badger",
    "Raven",
    "Eagle",
    "Falcon",
    # Extended landmarks
    "Tower",
    "Bridge",
    "Gate",
    "Keep",
    "Fort",
    "Haven",
    "Cove",
    "Bay",
    "Peak",
    "Pass",
)

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_AGENT_NAME_RE = re.compile(r"[^A-Za-z0-9]+")


def slugify(value: str) -> str:
    """Normalize a human-readable value into a slug."""
    normalized = value.strip().lower()
    slug = _SLUG_RE.sub("-", normalized).strip("-")
    return slug or "project"


def generate_agent_name() -> str:
    """Return a random adjective+noun combination."""
    adjective = random.choice(tuple(ADJECTIVES))
    noun = random.choice(tuple(NOUNS))
    return f"{adjective}{noun}"


def validate_agent_name_format(name: str) -> bool:
    """
    Validate that an agent name matches the required adjective+noun format.

    CRITICAL: Agent names MUST be randomly generated two-word combinations
    like "GreenLake" or "BlueDog", NOT descriptive names like "BackendHarmonizer".

    Names should be:
    - Unique and easy to remember
    - NOT descriptive of the agent's role or task
    - One of the predefined adjective+noun combinations (optionally with numeric suffix)

    Accepts formats:
    - "GreenLake" (base adjective+noun)
    - "GreenLake42" (with numeric suffix for uniqueness)

    Note: This validation is case-insensitive to match the database behavior
    where "GreenLake", "greenlake", and "GREENLAKE" are treated as the same.

    Returns True if valid, False otherwise.
    """
    if not name:
        return False

    # Strip trailing digits to check base name
    name_lower = name.lower()
    base_name = name_lower.rstrip("0123456789")

    # Check if base matches any valid adjective+noun combination (case-insensitive)
    for adjective in ADJECTIVES:
        for noun in NOUNS:
            if base_name == f"{adjective}{noun}".lower():
                return True

    return False


def generate_agent_name_with_suffix(suffix: int) -> str:
    """Return a random adjective+noun combination with numeric suffix."""
    adjective = random.choice(tuple(ADJECTIVES))
    noun = random.choice(tuple(NOUNS))
    return f"{adjective}{noun}{suffix}"


def sanitize_agent_name(value: str) -> Optional[str]:
    """Normalize user-provided agent name; return None if nothing remains."""
    cleaned = _AGENT_NAME_RE.sub("", value.strip())
    if not cleaned:
        return None
    return cleaned[:128]
