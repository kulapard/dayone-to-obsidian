import re
from functools import cached_property
from pathlib import Path

from dayone_to_obsidian.models import Entry
from dayone_to_obsidian.options import DEFAULT_OPTIONS, Options

from .media.audio import AudioProcessor
from .media.pdf import PdfProcessor
from .media.photo import PhotoProcessor
from .media.video import VideoProcessor
from .utils import ensure_dir, get_google_map_link, humanize_location, shorten_by_word

_CONTENT_TEMPLATE = """\
---
{header}
---
{body}

{footer}
"""

Processor = AudioProcessor | PhotoProcessor | VideoProcessor | PdfProcessor
MEDIA_PROCESSORS: list[type[Processor]] = [
    AudioProcessor,
    PhotoProcessor,
    VideoProcessor,
    PdfProcessor,
]


class EntryProcessor:
    def __init__(
        self,
        *,
        entry: Entry,
        root_dir: Path,
        journal_dir: Path,
        options: Options = DEFAULT_OPTIONS,
    ):
        self.entry = entry
        self.root_dir = root_dir
        self.journal_dir = journal_dir
        self.options = options

    @cached_property
    def entry_dir(self) -> Path:
        year_dir = self.journal_dir / str(self.entry.creationDate.year)
        month_dir = year_dir / self.entry.creationDate.strftime("%Y-%m")
        ensure_dir(month_dir)
        return month_dir

    def run(self) -> None:
        entry_content = self.get_entry_content()
        self.save(entry_content)

    def save(self, entry_content: str) -> None:
        entry_file_name = self.get_filename()
        entry_file_path = self.entry_dir / entry_file_name

        # If the file already exists, add a suffix
        duplicate_count = 0
        while entry_file_path.exists():
            duplicate_count += 1
            entry_file_name = self.get_filename(suffix=f" {duplicate_count}")
            entry_file_path = self.entry_dir / entry_file_name

        # Create the entry file
        entry_content = self.get_entry_content()
        with entry_file_path.open("w", encoding="utf-8") as f:
            f.writelines(entry_content)

    def get_filename(self, suffix: str = "") -> str:
        title = self.get_title()
        local_date_str = self.entry.creation_local_date.strftime("%Y-%m-%d")
        return f"[{local_date_str}] {title}{suffix}.md"

    def get_title(self) -> str:
        if not self.entry.text:
            return self.options.default_filename

        # Split the text into lines
        lines = self.entry.text.split("\n")

        # Find the first line that doesn't start with ![]
        title = ""
        for line in lines:
            if line and not line.startswith("!["):
                title = line
                break

        title = title.strip()

        if not title:
            return self.options.default_filename

        # Remove all markdown headers
        title = re.sub(r"^#+\s*", "", title)

        # Replace disallowed characters with spaces
        title = re.sub(r'[\\/:\*\?"<>|#^\[\]]', " ", title).strip()

        # shorten to 30 characters
        return shorten_by_word(title, max_length=30)

    def get_entry_content(self) -> str:
        content = _CONTENT_TEMPLATE.format(
            header=self.get_header(),
            body=self.get_body(),
            footer=self.get_footer(),
        )
        return content

    def get_header(self) -> str:
        headers: list[dict[str, str]] = [
            {"date": self.entry.creation_local_date_str},
            {"time zone": self.entry.timeZone},
        ]

        # Add weather
        weather = self.get_weather()
        if weather:
            headers.append({"weather": weather})

        # Add location
        humanized_location = self.get_humanized_location()
        if humanized_location:
            headers.append({"location": humanized_location})

        # Add tags
        tags = self.get_tags(tag_prefix=self.options.tag_prefix)
        tags.extend(list(self.options.additional_tags))
        if tags:
            headers.append({"tags": ", ".join(tags)})

        header = "\n".join(
            [f"{k}: {v}" for header in headers for k, v in header.items()],
        )
        return header

    def get_body(self) -> str:
        if not self.entry.text:
            return ""

        # Replace special characters
        body = self.entry.text.replace("\\", "")
        body = body.replace("\u2028", "\n")
        body = body.replace("\u1C6A", "\n\n")

        # Run media processors to replace media links
        body = self.run_media_processors(body)
        return body

    def run_media_processors(self, body: str) -> str:
        for MediaProcessor in MEDIA_PROCESSORS:
            body = MediaProcessor(
                entry=self.entry, root_dir=self.root_dir, entry_dir=self.entry_dir
            ).run(body)

        return body

    def get_footer(self) -> str:
        footer = ""
        footer_rows = []

        # Add GPS coordinates
        if self.entry.location:
            lon = self.entry.location.longitude
            lat = self.entry.location.latitude
            location_name = self.get_humanized_location()

            google_map_link = get_google_map_link(lon, lat)
            footer_rows.append(f"[{location_name}]({google_map_link})")

        footer = "\n".join(footer_rows)
        return footer

    def get_weather(self) -> str:
        weather = ""
        if self.entry.weather:
            temperature = int(self.entry.weather.temperatureCelsius)
            description = self.entry.weather.conditionsDescription
            if self.entry.location and self.entry.location.localityName:
                weather_location = self.entry.location.localityName
                weather += f"{weather_location} "

            weather += f"{temperature}°C {description}"
        return weather

    def get_tags(self, tag_prefix: str) -> list[str]:
        tags = []
        for t in self.entry.tags:
            if not t:
                # Skip empty tags
                continue

            safe_tag = t.replace(" ", "-").replace("---", "-")
            tags.append(f"{tag_prefix}{safe_tag}")
            if self.entry.starred:
                tags.append(f"{tag_prefix}starred")

        return tags

    def get_humanized_location(self) -> str:
        return humanize_location(self.entry.location) if self.entry.location else ""
