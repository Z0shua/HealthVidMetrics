import pytest
from src.healthvidmetrics.youtube_api import extract_video_id, convert_duration_to_seconds

def test_extract_video_id():
    urls = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s", "dQw4w9WgXcQ"),
        ("invalid_url", None)
    ]
    for url, expected in urls:
        assert extract_video_id(url) == expected

def test_convert_duration_to_seconds():
    cases = [
        ("PT1H2M30S", 3750),
        ("PT5M", 300),
        ("PT30S", 30),
        ("PT1H", 3600),
        ("PT0S", 0),
        ("", 0),
    ]
    for duration, expected in cases:
        try:
            result = convert_duration_to_seconds(duration)
        except Exception:
            result = 0
        assert result == expected 