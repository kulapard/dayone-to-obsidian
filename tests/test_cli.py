from pathlib import Path

from click.testing import CliRunner

from dayone_to_obsidian import cli
from dayone_to_obsidian.version import __version__
from tests.constants import INVALID_JSON_PATH, JOURNAL_JSON_PATH


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli.main, ["version"])
    assert result.exit_code == 0, result.output
    assert result.output == __version__ + "\n"


def test_run_empty():
    runner = CliRunner()
    result = runner.invoke(cli.main, ["run"])
    assert result.exit_code == 0, result.output
    assert "Found 0 JSON files to process" in result.output


def test_run_ok(tmp_dir: Path):
    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["run", "--json", str(JOURNAL_JSON_PATH), "--target", str(tmp_dir)]
    )
    assert result.exit_code == 0, result.output
    assert "Found 1 JSON files to process" in result.output
    assert "Processed 1 entries" in result.output


def test_run_force(tmp_dir: Path):
    runner = CliRunner()

    # Run once to create the journal
    result = runner.invoke(
        cli.main, ["run", "--json", str(JOURNAL_JSON_PATH), "--target", str(tmp_dir)]
    )
    assert result.exit_code == 0, result.output
    assert "Found 1 JSON files to process" in result.output
    assert "Processed 1 entries" in result.output

    # Run again to test force
    result = runner.invoke(
        cli.main, ["run", "--json", str(JOURNAL_JSON_PATH), "--target", str(tmp_dir)]
    )
    assert result.exit_code == 1, result.output
    assert "Journal folder already exists" in result.output

    # Run again with force
    result = runner.invoke(
        cli.main, ["run", "--json", str(JOURNAL_JSON_PATH), "--target", str(tmp_dir), "--force"]
    )
    assert result.exit_code == 0, result.output
    assert "Force overwrite of existing journal folder" in result.output
    assert "Found 1 JSON files to process" in result.output
    assert "Processed 1 entries" in result.output


def test_run_invalid_json(tmp_dir: Path):
    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["run", "--json", str(INVALID_JSON_PATH), "--target", str(tmp_dir)]
    )
    assert result.exit_code == 1, result.output
    assert "Invalid DayOne journal file" in result.output
