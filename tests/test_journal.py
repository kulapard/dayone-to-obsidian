from pathlib import Path

from dayone_to_obsidian.models import Journal
from dayone_to_obsidian.options import DEFAULT_OPTIONS, Options
from dayone_to_obsidian.processors.journal import JournalProcessor
from tests.constants import ASSETS_DIR


def test_journal_processor(tmp_dir: Path):
    journal_json_path = ASSETS_DIR / "journal.json"

    # Load with default options
    p = JournalProcessor.load(json_path=journal_json_path)

    assert isinstance(p.journal, Journal)
    assert p.json_path == ASSETS_DIR / "journal.json"
    assert p.options == DEFAULT_OPTIONS
    assert p.root_dir == ASSETS_DIR
    assert p.journal_dir == Path("export/journal")  # default

    # Load with custom options
    options = Options(
        target_dir=tmp_dir / "custom" / "target",
        tag_prefix="custom",
        additional_tags=["foo", "bar"],
        default_filename="custom",
    )
    p = JournalProcessor.load(json_path=journal_json_path, options=options)

    assert isinstance(p.journal, Journal)
    assert p.json_path == ASSETS_DIR / "journal.json"
    assert p.options == options
    assert p.root_dir == ASSETS_DIR
    assert p.journal_dir == tmp_dir / "custom" / "target" / "journal"
