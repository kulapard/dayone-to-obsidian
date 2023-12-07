from dayone_to_obsidian.models import Location
from dayone_to_obsidian.processors.utils import (
    humanize_duration,
    humanize_location,
    shorten_by_word,
)


def test_humanize_time():
    assert humanize_duration(123.123) == "2 minutes 3 seconds"
    assert humanize_duration(1234.123) == "20 minutes 34 seconds"
    assert humanize_duration(12345.123) == "3 hours 25 minutes 45 seconds"
    assert humanize_duration(123456.123) == "34 hours 17 minutes 36 seconds"
    assert humanize_duration(1234567.123) == "342 hours 56 minutes 7 seconds"
    assert humanize_duration(12345678.123) == "3429 hours 21 minutes 18 seconds"


def test_humanize_location():
    # If userLabel is not present, use placeName, localityName, administrativeArea, and country
    # If administrativeArea is the same as localityName, ignore it
    location = Location(
        userLabel=None,
        placeName="221B Baker Street",
        localityName="London",
        administrativeArea="London",
        country="UK",
        longitude=12.34,
        latitude=56.78,
    )
    assert humanize_location(location) == "221B Baker Street, London, UK"

    # If userLabel is present, use it
    location = Location(
        userLabel="221B Baker Street",
        placeName="ignore it",
        localityName="Central London",
        administrativeArea="London",
        country="UK",
        longitude=12.34,
        latitude=56.78,
    )
    assert humanize_location(location) == "221B Baker Street, Central London, London, UK"


def test_shorten_by_word():
    assert shorten_by_word("1 2 3 4", max_length=5) == "1 2"
    assert shorten_by_word("one two three", max_length=5) == "one"
    assert shorten_by_word("one two three", max_length=10) == "one two"
