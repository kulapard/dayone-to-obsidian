from dayone_to_obsidian.models import Photo
from dayone_to_obsidian.processors.utils import humanize_location

from .base import AbstractMediaProcessor


class PhotoProcessor(AbstractMediaProcessor[Photo]):
    source_media_dir_name = "photos"
    entry_media_dir_name = "assets"

    def get_medias(self) -> list[Photo]:
        return self.entry.photos

    def get_old_link(self, media: Photo) -> str:
        return f"![](dayone-moment://{media.identifier})"

    def get_new_link(self, media: Photo) -> str:
        return f"![]({self.entry_media_dir_name}/{media.file_name})"

    def get_meta_data(self, media: Photo) -> str:
        meta: list[str] = []

        if media.date:
            meta.append(f"Date: {media.date}")

        if media.location:
            location_str = humanize_location(media.location)
            meta.append(f"Location: {location_str}")

        return "\n".join(meta)
