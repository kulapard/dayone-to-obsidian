import abc
import shutil
from pathlib import Path
from typing import Generic, TypeVar

from dayone_to_obsidian.models import Audio, Entry, Pdf, Photo, Video
from dayone_to_obsidian.processors.utils import ensure_dir

MediaType = TypeVar("MediaType", bound=Audio | Photo | Video | Pdf)


class MediaFileNotFoundError(Exception):
    def __init__(self, media_file_path: Path):
        self.media_file_path = media_file_path
        super().__init__(f"Media file not found: {media_file_path}")


class AbstractMediaProcessor(abc.ABC, Generic[MediaType]):
    def __init__(self, *, entry: Entry, root_dir: Path, entry_dir: Path):
        self.entry = entry
        self.root_dir = root_dir
        self.entry_dir = entry_dir

    @property
    @abc.abstractmethod
    def source_media_dir_name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def entry_media_dir_name(self) -> str:
        ...

    @abc.abstractmethod
    def get_medias(self) -> list[MediaType]:
        ...

    @abc.abstractmethod
    def get_old_link(self, media: MediaType) -> str:
        ...

    @abc.abstractmethod
    def get_new_link(self, media: MediaType) -> str:
        ...

    @abc.abstractmethod
    def get_meta_data(self, media: MediaType) -> str:
        ...

    def run(self, body: str) -> str:
        medias = self.get_medias()

        if not medias:
            # No medias, nothing to do
            return body

        for media in medias:
            self.copy_media(media)

            old_link = self.get_old_link(media)
            new_link = self.get_new_link(media)

            meta_data = self.get_meta_data(media)
            if meta_data:
                new_link += "\n"
                new_link += meta_data

            body = body.replace(old_link, new_link)

        return body

    def copy_media(self, media: MediaType) -> None:
        entry_media_dir = self.entry_dir / self.entry_media_dir_name
        source_media_dir = self.root_dir / self.source_media_dir_name

        # Copy the media file
        old_media_path = source_media_dir / media.file_name
        new_media_path = entry_media_dir / media.file_name

        if not old_media_path.exists():
            raise MediaFileNotFoundError(old_media_path)

        ensure_dir(new_media_path.parent)
        shutil.copy(old_media_path, new_media_path)
