from src.healthvidmetrics.config import load_api_keys

def test_load_api_keys(monkeypatch):
    monkeypatch.setenv("YOUTUBE_API_KEY", "ytkey")
    monkeypatch.setenv("OPENAI_API_KEY", "oakey")
    yt, oa = load_api_keys()
    assert yt == "ytkey"
    assert oa == "oakey" 