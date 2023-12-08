from click.testing import CliRunner

from dayone_to_obsidian import __version__, cli


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli.main, ["version"])
    assert result.exit_code == 0, result.output
    assert result.output == __version__ + "\n"
