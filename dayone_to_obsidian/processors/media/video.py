from dayone_to_obsidian.models import Video
from dayone_to_obsidian.processors.utils import humanize_location

from .base import AbstractMediaProcessor


class VideoProcessor(AbstractMediaProcessor):
    source_media_dir_name = "videos"
    entry_media_dir_name = "media/video"

    def get_medias(self) -> list[Video]:
        return self.entry.videos

    def get_old_link(self, media: Video) -> str:
        return f"![](dayone-moment:/video/{media.identifier})"

    def get_new_link(self, media: Video) -> str:
        return f"![]({self.entry_media_dir_name}/{media.file_name})"

    def get_meta_data(self, media: Video) -> str:
        meta: list[str] = []

        if media.title:
            meta.append(f"Title: {media.title}")

        # TODO: human readable duration
        if media.duration:
            meta.append(f"Duration: {media.duration}")

        if media.date:
            meta.append(f"Date: {media.date}")

        if media.location:
            location_str = humanize_location(media.location)
            meta.append(f"Location: {location_str}")

        return "\n".join(meta)
