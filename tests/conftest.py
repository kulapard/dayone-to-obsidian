import tempfile
from pathlib import Path

import pytest

from dayone_to_obsidian.models import Entry
from tests.constants import ENTRY_JSON_PATH


@pytest.fixture
def entry() -> Entry:
    with ENTRY_JSON_PATH.open(encoding="utf-8") as json_file:
        return Entry.model_validate_json(json_file.read())


@pytest.fixture
def tmp_dir() -> Path:
    """Create a temporary directory and return its path. Delete the directory when the test finishes."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)
