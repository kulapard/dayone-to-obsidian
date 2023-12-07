import os
from pathlib import Path

from dayone_to_obsidian.models import Location


def ensure_dir(path: Path) -> None:
    if not path.exists():
        os.makedirs(path)


def shorten_by_word(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text

    words = text.split(" ")
    shortened_words: list[str] = []
    for word in words:
        res_candidate = " ".join(shortened_words + [word])
        # +1 for the space
        if len(res_candidate) + 1 > max_length:
            break

        shortened_words.append(word)
    return " ".join(shortened_words)


def humanize_location(location: Location) -> str:
    # Add location
    locations = []

    # Pick only one place name to avoid repetition
    if location.userLabel:
        locations.append(location.userLabel)
    elif location.placeName:
        locations.append(location.placeName)

    # Add other location info
    if location.localityName:
        locations.append(location.localityName)

    if location.administrativeArea and location.administrativeArea != location.localityName:
        locations.append(location.administrativeArea)

    if location.country:
        locations.append(location.country)

    return ", ".join(locations)


def get_google_map_link(longitude: float, latitude: float) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"


def humanize_duration(total_seconds: float) -> str:
    """Convert a time in seconds to a human-readable format"""
    # Calculate hours, minutes, and seconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours} hours")

    if minutes > 0:
        parts.append(f"{minutes} minutes")

    if seconds > 0:
        parts.append(f"{seconds:.0f} seconds")

    duration = " ".join(parts)
    return duration
