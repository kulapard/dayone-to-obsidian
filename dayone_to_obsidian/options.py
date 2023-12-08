from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, kw_only=True)
class Options:
    target_dir: Path | None = None
    tag_prefix: str = ""
    additional_tags: list[str] = field(default_factory=list)
    default_filename: str = "Untitled"

    def __repr__(self) -> str:
        params = "\n".join(f" - {k} = {v!s}" for k, v in self.__dict__.items())
        return f"Options:\n{params}"


DEFAULT_OPTIONS = Options()
