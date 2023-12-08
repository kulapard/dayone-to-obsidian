from datetime import datetime, tzinfo

from dateutil import tz
from pydantic import BaseModel, Field


class Weather(BaseModel):
    temperatureCelsius: float
    weatherServiceName: str
    windBearing: int
    conditionsDescription: str
    relativeHumidity: int
    weatherCode: str
    pressureMB: float
    windSpeedKPH: float
    windChillCelsius: float | None = None
    sunriseDate: datetime | None = None
    sunsetDate: datetime | None = None

    moonPhase: float | None = None
    moonPhaseCode: str | None = None


class Location(BaseModel):
    country: str
    administrativeArea: str
    placeName: str
    longitude: float
    latitude: float
    userLabel: str | None = None
    localityName: str | None = None


class Photo(BaseModel):
    md5: str
    identifier: str
    type: str
    fileSize: int
    orderInEntry: int
    creationDevice: str
    duration: int
    favorite: bool
    height: int
    width: int
    isSketch: bool

    date: datetime | None = None
    exposureBiasValue: float | None = None
    fnumber: str | None = None
    focalLength: str | None = None

    cameraModel: str | None = None
    cameraMake: str | None = None
    lensMake: str | None = None
    lensModel: str | None = None

    location: Location | None = None

    @property
    def file_name(self) -> str:
        return f"{self.md5}.{self.type}"


class Audio(BaseModel):
    md5: str
    identifier: str
    format: str
    fileSize: int
    orderInEntry: int
    title: str
    creationDevice: str
    audioChannels: str
    duration: float
    favorite: bool
    height: int
    width: int
    sampleRate: str
    timeZoneName: str

    date: datetime | None = None
    location: Location | None = None

    @property
    def file_name(self) -> str:
        return f"{self.md5}.m4a"


class Video(BaseModel):
    md5: str
    identifier: str
    type: str
    favorite: bool
    fileSize: int
    orderInEntry: int
    width: int
    height: int
    creationDevice: str
    duration: float

    date: datetime | None = None
    title: str | None = None
    location: Location | None = None

    @property
    def file_name(self) -> str:
        return f"{self.md5}.{self.type}"


# TODO: Add other fields (pdf attachments available only on DayOne Premium subscription)
class Pdf(BaseModel):
    md5: str
    identifier: str

    pdfName: str | None = None
    date: datetime | None = None
    location: Location | None = None

    @property
    def file_name(self) -> str:
        return f"{self.md5}.pdf"


class Entry(BaseModel):
    starred: bool
    modifiedDate: datetime
    uuid: str
    isPinned: bool
    creationDate: datetime
    isAllDay: bool
    timeZone: str
    text: str | None = None

    creationDeviceType: str | None = None
    creationOSName: str | None = None
    creationDevice: str | None = None

    richText: str | None = None
    duration: int | None = None
    location: Location | None = None
    tags: list[str] = Field(default_factory=list)
    weather: Weather | None = None

    photos: list[Photo] = Field(default_factory=list)
    audios: list[Audio] = Field(default_factory=list)
    videos: list[Video] = Field(default_factory=list)
    pdfAttachments: list[Pdf] = Field(default_factory=list)

    creationDeviceModel: str | None = None
    editingTime: float | None = None
    creationOSVersion: str | None = None

    @property
    def tz(self) -> tzinfo | None:
        return tz.gettz(self.timeZone)

    @property
    def creation_local_date(self) -> datetime:
        return self.creationDate.astimezone(tz=self.tz)

    @property
    def creation_local_date_str(self) -> str:
        # Format the date and time with the weekday
        return self.creation_local_date.strftime("%Y-%m-%d %H:%M:%S %A")


class Metadata(BaseModel):
    version: str


class Journal(BaseModel):
    entries: list[Entry]
    metadata: Metadata
