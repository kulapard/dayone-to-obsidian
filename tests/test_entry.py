from pathlib import Path

from dayone_to_obsidian.models import Entry
from dayone_to_obsidian.processors.entry import EntryProcessor
from tests.constants import ASSETS_DIR


def test_entry_processor(entry: Entry, tmp_dir: Path):
    p = EntryProcessor(
        entry=entry,
        root_dir=ASSETS_DIR,
        journal_dir=tmp_dir,
    )

    assert p.entry == entry
    assert p.root_dir == ASSETS_DIR
    assert p.journal_dir == tmp_dir
    assert p.entry_dir == tmp_dir / "2018" / "2018-04"
    assert p.get_filename() == "[2018-04-21] test text.md"
    assert p.get_title() == "test text"
    assert p.get_header() == (
        "date: 2018-04-21 18:57:04 Saturday\n"
        "time zone: Europe/London\n"
        "weather: London 11°C Mostly Cloudy\n"
        "location: 221B Baker Street, London, UK"
    )
    assert p.get_body() == "test text"
    assert p.get_footer() == (
        "[221B Baker Street, London, UK](https://www.google.com/maps/search/?api=1&query=51.523788,-0.158611)"
    )
    assert p.get_entry_content() == (
        "---\n"
        "date: 2018-04-21 18:57:04 Saturday\n"
        "time zone: Europe/London\n"
        "weather: London 11°C Mostly Cloudy\n"
        "location: 221B Baker Street, London, UK\n"
        "---\n"
        "test text\n"
        "\n"
        "[221B Baker Street, London, UK](https://www.google.com/maps/search/?api=1&query=51.523788,-0.158611)\n"
    )
