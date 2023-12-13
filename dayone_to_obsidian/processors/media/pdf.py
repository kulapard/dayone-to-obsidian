from dayone_to_obsidian.models import Pdf
from dayone_to_obsidian.processors.utils import humanize_location

from .base import AbstractMediaProcessor


class PdfProcessor(AbstractMediaProcessor[Pdf]):
    source_media_dir_name = "pdfs"
    entry_media_dir_name = "assets"

    def get_medias(self) -> list[Pdf]:
        return self.entry.pdfAttachments

    def get_old_link(self, media: Pdf) -> str:
        return f"![](dayone-moment:/pdfAttachment/{media.identifier})"

    def get_new_link(self, media: Pdf) -> str:
        return f"![]({self.entry_media_dir_name}/{media.file_name})"

    def get_meta_data(self, media: Pdf) -> str:
        meta: list[str] = []

        if media.pdfName:
            meta.append(f"Title: {media.pdfName}")

        if media.date:
            meta.append(f"Date: {media.date}")

        if media.location:
            location_str = humanize_location(media.location)
            meta.append(f"Location: {location_str}")

        return "\n".join(meta)
