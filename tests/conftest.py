import tempfile
from pathlib import Path

import pytest

from dayone_to_obsidian.models import Entry, Journal
from tests.constants import JOURNAL_JSON_PATH


@pytest.fixture(scope="session")
def journal() -> Journal:
    with JOURNAL_JSON_PATH.open(encoding="utf-8") as json_file:
        return Journal.model_validate_json(json_file.read())


@pytest.fixture(scope="session")
def entry(journal: Journal) -> Entry:
    return journal.entries[0]


@pytest.fixture
def tmp_dir() -> Path:
    """Create a temporary directory and return its path. Delete the directory when the test finishes."""
    with tempfile.TemporaryDirectory() as t:
        yield Path(t).resolve()
