import shutil
from functools import cached_property
from pathlib import Path

import click
from pydantic import ValidationError

from dayone_to_obsidian.helpers import echo_red, echo_yellow
from dayone_to_obsidian.models import Journal
from dayone_to_obsidian.options import DEFAULT_OPTIONS, Options

from .entry import EntryProcessor


class ErrorLoadingJournal(Exception):
    pass


class JournalDirAlreadyExists(Exception):
    def __init__(self, journal_dir: Path):
        self.journal_dir = journal_dir
        super().__init__(f"Journal folder already exists: {journal_dir}")


class JournalProcessor:
    def __init__(self, *, journal: Journal, json_path: Path, options: Options):
        self.journal = journal
        self.json_path = json_path
        self.options = options

    @classmethod
    def load(cls, *, json_path: Path, options: Options = DEFAULT_OPTIONS) -> "JournalProcessor":
        with json_path.open(encoding="utf-8") as json_file:
            try:
                journal = Journal.model_validate_json(json_file.read())
            except ValidationError as e:
                echo_red(f"Invalid DayOne journal file: {json_path}: {e}")
                raise ErrorLoadingJournal from e

        return cls(journal=journal, json_path=json_path, options=options)

    @cached_property
    def root_dir(self) -> Path:
        """Path to the root directory. Same as the journal directory."""
        return self.json_path.parent

    @cached_property
    def target_dir(self) -> Path:
        """Path to the target directory. By default, it's the same as the JSON directory."""
        return self.options.target_dir or self.json_path.parent

    @cached_property
    def journal_dir(self) -> Path:
        journal_dir_name = self.json_path.name.split(".")[0]
        journal_dir = self.target_dir / journal_dir_name
        journal_dir = journal_dir.resolve()
        return journal_dir

    def run(self, force: bool) -> None:
        click.echo(f"Journal dir: {self.journal_dir}")

        if force and self.journal_dir.exists():
            echo_yellow("Force overwrite of existing journal folder.")
            shutil.rmtree(self.journal_dir)
        else:
            click.echo("Checking if journal folder already exists.")
            if self.journal_dir.exists():
                raise JournalDirAlreadyExists(self.journal_dir)

        processed_count = 0
        for entry in self.journal.entries:
            EntryProcessor(
                entry=entry,
                root_dir=self.root_dir,
                journal_dir=self.journal_dir,
                options=self.options,
            ).run()
            processed_count += 1

        echo_yellow(f"Processed {processed_count} entries")
