from pathlib import Path

import click

from dayone_to_obsidian.helpers import echo_green, echo_red
from dayone_to_obsidian.options import DEFAULT_OPTIONS, Options
from dayone_to_obsidian.processors.journal import ErrorLoadingJournal, JournalProcessor
from dayone_to_obsidian.processors.media.base import MediaFileNotFoundError


@click.group()
def main() -> None:
    pass


@main.command()
def version() -> None:
    """Show the program's version number and exit."""
    from . import __version__

    click.echo(__version__)


@main.command()
@click.option(
    "--json",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, path_type=Path),
    help="Path to the DayOne JSON file or directory with JSON files (e.g.: Journal.json or ./DayOneExport). By default it will look for JSON files in the current directory.",
    default=Path("."),
)
@click.option(
    "--force",
    is_flag=True,
    help="Force overwrite of existing journal folder.",
)
@click.option(
    "--target",
    "target_dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Path to the target directory where the converted files will be stored. By default it will create a new folder in the current directory.",
    default=DEFAULT_OPTIONS.target_dir,
)
@click.option(
    "--tag-prefix",
    "tag_prefix",
    type=str,
    help="Prefix for tags. By default it will use `DayOne`.",
    default=DEFAULT_OPTIONS.tag_prefix,
)
def run(json: Path, target_dir: Path, force: bool, tag_prefix: str) -> None:
    """
    Convert your DayOne journal entries into Obsidian-ready markdown files.
    """
    options = Options(tag_prefix=tag_prefix)

    if json.is_file():
        json_files = [json]
    elif json.is_dir():
        json_files = list(json.glob("*.json"))
    else:
        echo_red(f"Invalid JSON path: {json}")
        return

    if not target_dir.exists():
        # Create target directory if it doesn't exist
        echo_green(f"Creating target directory: {target_dir}")
        target_dir.mkdir(parents=True)

    click.echo(f"Found {len(json_files)} JSON files to process")  # noqa: T201

    for json_path in json_files:
        echo_green(f"Processing `{json_path}`")
        try:
            JournalProcessor.load(json_path=json_path, options=options).run(force=force)
        except ErrorLoadingJournal:
            echo_red(f"Error loading DayOne journal: {json_path}")
        except MediaFileNotFoundError as e:
            echo_red(f"Media file not found: {e}")


if __name__ == "__main__":
    main()
