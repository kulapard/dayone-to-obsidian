from pathlib import Path

from dayone_to_obsidian.models import Journal
from dayone_to_obsidian.options import DEFAULT_OPTIONS, Options
from dayone_to_obsidian.processors.journal import JournalProcessor
from tests.constants import ASSETS_DIR, JOURNAL_JSON_PATH


def test_journal_processor(tmp_dir: Path):
    # Load with default options
    p = JournalProcessor.load(json_path=JOURNAL_JSON_PATH)

    assert isinstance(p.journal, Journal)
    assert p.json_path == ASSETS_DIR / "MyJournal.json"
    assert p.options == DEFAULT_OPTIONS
    assert p.root_dir == ASSETS_DIR
    # by default, target_dir is the same as the JSON directory
    assert p.journal_dir == ASSETS_DIR / "MyJournal"

    # Load with custom options
    options = Options(
        target_dir=tmp_dir / "custom" / "target",
        tag_prefix="custom_tag_prefix/",
        additional_tags=["foo", "bar"],
        default_filename="custom_filename",
    )
    p = JournalProcessor.load(json_path=JOURNAL_JSON_PATH, options=options)

    assert isinstance(p.journal, Journal)
    assert p.json_path == ASSETS_DIR / "MyJournal.json"
    assert p.options == options
    assert p.root_dir == ASSETS_DIR
    assert p.journal_dir == tmp_dir / "custom" / "target" / "MyJournal"
