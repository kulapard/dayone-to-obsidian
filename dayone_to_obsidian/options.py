from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, kw_only=True)
class Options:
    target_dir: Path | None = None
    tag_prefix: str = ""
    additional_tags: Iterable[str] = field(default_factory=list)
    default_filename: str = "Untitled"


DEFAULT_OPTIONS = Options()
