import shutil
from functools import cached_property
from pathlib import Path

import click
from pydantic import ValidationError

from dayone_to_obsidian.models import Journal

from ..helpers import echo_red, echo_yellow
from ..options import Options
from .entry import EntryProcessor
from .utils import ensure_dir


class ErrorLoadingJournal(Exception):
    pass


class JournalProcessor:
    def __init__(self, *, journal: Journal, json_path: Path, options: Options):
        self.journal = journal
        self.json_path = json_path
        self.options = options

    @classmethod
    def load(cls, *, json_path: Path, options: Options) -> "JournalProcessor":
        with json_path.open(encoding="utf-8") as json_file:
            try:
                journal = Journal.model_validate_json(json_file.read())
            except ValidationError as e:
                echo_red(f"Invalid DayOne journal file: {json_path}: {e}")
                raise ErrorLoadingJournal from e

        return cls(journal=journal, json_path=json_path, options=options)

    @property
    def root_dir(self) -> Path:
        """Path to the root directory. Same as the journal directory."""
        return self.json_path.parent

    @cached_property
    def journal_dir(self) -> Path:
        journal_dir_name = self.json_path.name.split(".")[0]
        journal_dir = self.options.target_dir / journal_dir_name
        ensure_dir(journal_dir)
        return journal_dir

    def run(self, force: bool) -> None:
        click.echo(f"Journal dir: {self.journal_dir}")

        if force:
            click.echo("Force overwrite of existing journal folder.")
            shutil.rmtree(self.journal_dir)
        else:
            click.echo("Checking if journal folder already exists.")
            if self.journal_dir.exists():
                echo_red(
                    f"Journal folder already exists: {self.journal_dir}. Use --force to overwrite."
                )
                return

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
