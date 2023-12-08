from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.resolve()
TESTS_DIR = PROJECT_DIR / "tests"
ASSETS_DIR = TESTS_DIR / "assets"
JOURNAL_JSON_PATH = ASSETS_DIR / "MyJournal.json"
INVALID_JSON_PATH = ASSETS_DIR / "invalid.json"
