from dayone_to_obsidian.models import Audio
from dayone_to_obsidian.processors.utils import humanize_duration, humanize_location

from .base import AbstractMediaProcessor


class AudioProcessor(AbstractMediaProcessor[Audio]):
    source_media_dir_name = "audios"
    entry_media_dir_name = "assets"

    def get_medias(self) -> list[Audio]:
        return self.entry.audios

    def get_old_link(self, media: Audio) -> str:
        return f"![](dayone-moment:/audio/{media.identifier})"

    def get_new_link(self, media: Audio) -> str:
        return f"![]({self.entry_media_dir_name}/{media.file_name})"

    def get_meta_data(self, media: Audio) -> str:
        meta: list[str] = []

        if media.title:
            meta.append(f"Title: {media.title}")

        if media.duration:
            duration = humanize_duration(media.duration)
            meta.append(f"Duration: {duration}")

        if media.date:
            meta.append(f"Date: {media.date}")

        if media.creationDevice:
            meta.append(f"Device: {media.creationDevice}")

        if media.location:
            location_str = humanize_location(media.location)
            meta.append(f"Location: {location_str}")

        return "\n".join(meta)
