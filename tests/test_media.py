from pathlib import Path

from dayone_to_obsidian.models import Entry
from dayone_to_obsidian.processors.media.audio import AudioProcessor
from dayone_to_obsidian.processors.media.pdf import PdfProcessor
from dayone_to_obsidian.processors.media.photo import PhotoProcessor
from dayone_to_obsidian.processors.media.video import VideoProcessor


def test_photo_processor(entry: Entry, tmp_dir: Path):
    p = PhotoProcessor(
        entry=entry,
        root_dir=tmp_dir,
        entry_dir=tmp_dir / "entry_dir",
    )

    assert p.entry == entry
    assert p.root_dir == tmp_dir
    assert p.entry_dir == tmp_dir / "entry_dir"
    assert p.get_medias() == entry.photos
    assert p.source_media_dir_name == "photos"
    assert p.entry_media_dir_name == "assets"

    photo = entry.photos[0]
    assert p.get_old_link(photo) == f"![](dayone-moment://{photo.identifier})"
    assert p.get_new_link(photo) == f"![](assets/{photo.file_name})"
    assert p.get_meta_data(photo) == (
        "Date: 2018-04-21 14:30:59+00:00\n" "Location: 221B Baker Street, London, UK"
    )


def test_video_processor(entry: Entry, tmp_dir: Path):
    p = VideoProcessor(
        entry=entry,
        root_dir=tmp_dir,
        entry_dir=tmp_dir / "entry_dir",
    )

    assert p.entry == entry
    assert p.root_dir == tmp_dir
    assert p.entry_dir == tmp_dir / "entry_dir"
    assert p.get_medias() == entry.videos
    assert p.source_media_dir_name == "videos"
    assert p.entry_media_dir_name == "assets"

    video = entry.videos[0]
    assert p.get_old_link(video) == f"![](dayone-moment:/video/{video.identifier})"
    assert p.get_new_link(video) == f"![](assets/{video.file_name})"
    assert p.get_meta_data(video) == ("Duration: 15 seconds")


def test_audio_processor(entry: Entry, tmp_dir: Path):
    p = AudioProcessor(
        entry=entry,
        root_dir=tmp_dir,
        entry_dir=tmp_dir / "entry_dir",
    )

    assert p.entry == entry
    assert p.root_dir == tmp_dir
    assert p.entry_dir == tmp_dir / "entry_dir"
    assert p.get_medias() == entry.audios
    assert p.source_media_dir_name == "audios"
    assert p.entry_media_dir_name == "assets"

    audio = entry.audios[0]
    assert p.get_old_link(audio) == f"![](dayone-moment:/audio/{audio.identifier})"
    assert p.get_new_link(audio) == f"![](assets/{audio.file_name})"
    assert p.get_meta_data(audio) == (
        "Title: My Audio File.mp3\nDuration: 15 minutes 43 seconds\nDevice: My iPhone"
    )


def test_pdf_processor(entry: Entry, tmp_dir: Path):
    p = PdfProcessor(
        entry=entry,
        root_dir=tmp_dir,
        entry_dir=tmp_dir / "entry_dir",
    )

    assert p.entry == entry
    assert p.root_dir == tmp_dir
    assert p.entry_dir == tmp_dir / "entry_dir"
    assert p.get_medias() == entry.pdfAttachments
    assert p.source_media_dir_name == "pdfs"
    assert p.entry_media_dir_name == "assets"

    pdf = entry.pdfAttachments[0]
    assert p.get_old_link(pdf) == f"![](dayone-moment:/pdfAttachment/{pdf.identifier})"
    assert p.get_new_link(pdf) == f"![](assets/{pdf.file_name})"
    assert p.get_meta_data(pdf) == "Title: My PDF File.pdf"
