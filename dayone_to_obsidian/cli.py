from pathlib import Path

import click

from dayone_to_obsidian.helpers import echo_green
from dayone_to_obsidian.options import DEFAULT_OPTIONS, Options
from dayone_to_obsidian.processors.journal import (
    ErrorLoadingJournal,
    JournalDirAlreadyExists,
    JournalProcessor,
)
from dayone_to_obsidian.processors.media.base import MediaFileNotFoundError


@click.group()
def main() -> None:
    pass


@main.command()
def version() -> None:
    """Show the program's version number and exit."""
    from .version import __version__

    click.echo(__version__)


@main.command()
@click.option(
    "--json",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, path_type=Path),
    help="Path to the DayOne JSON file or directory with JSON files (e.g.: Journal.json or ./DayOneExport)."
    "By default it will look for JSON files in the current directory.",
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
    help="Path to the target directory where the converted files will be stored. "
    "By default it will create a new folder in the current directory.",
    default=DEFAULT_OPTIONS.target_dir,
)
@click.option(
    "--tag-prefix",
    "tag_prefix",
    type=str,
    help="Prefix for tags. By default it's empty. "
    "Example: `--tag-prefix=DayOne/` will convert `tag` to `DayOne/tag`.",
    default=DEFAULT_OPTIONS.tag_prefix,
)
@click.option(
    "--tag",
    "additional_tags",
    type=str,
    multiple=True,
    help="Additional tag to add to all entries. Can be specified multiple times."
    "Example: `--tag=DayOne --tag=Journal` will add `DayOne` and `Journal` tags to all entries.",
    default=DEFAULT_OPTIONS.additional_tags,
)
def run(
    json: Path, target_dir: Path, force: bool, tag_prefix: str, additional_tags: list[str]
) -> None:
    """
    Convert your DayOne journal entries into Obsidian-ready markdown files.
    """
    if json.is_dir():
        json_files = list(json.glob("*.json"))
    else:
        json_files = [json]

    if target_dir is None:
        target_dir = json.parent if json.is_dir() else json

    # Get an absolute path
    target_dir = target_dir.resolve()
    echo_green(f"Target directory: `{target_dir}`")

    options = Options(
        tag_prefix=tag_prefix, additional_tags=list(additional_tags), target_dir=target_dir
    )
    click.echo(options)
    click.echo(f"Found {len(json_files)} JSON files to process")  # noqa: T201

    for json_path in json_files:
        # Get an absolute path
        json_path = json_path.resolve()
        echo_green(f"Processing `{json_path}`")
        try:
            JournalProcessor.load(json_path=json_path, options=options).run(force=force)
        except ErrorLoadingJournal as e:
            raise click.ClickException(f"Error loading DayOne journal: {json_path}") from e
        except MediaFileNotFoundError as e:
            raise click.ClickException(f"Media file not found: {e.media_file_path}") from e
        except JournalDirAlreadyExists as e:
            raise click.ClickException(
                f"Journal folder already exists: {e.journal_dir}. Use --force to overwrite."
            ) from e


if __name__ == "__main__":
    main()
