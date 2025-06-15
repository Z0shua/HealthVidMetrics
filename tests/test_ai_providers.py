import pytest
from src.healthvidmetrics.ai_providers import create_ai_provider, OpenAIProvider

def test_create_ai_provider_openai():
    """Test creating OpenAI provider"""
    provider = create_ai_provider("openai", "test_key")
    assert isinstance(provider, OpenAIProvider)

def test_create_ai_provider_invalid():
    """Test creating invalid provider"""
    with pytest.raises(ValueError):
        create_ai_provider("invalid_provider", "test_key")

def test_openai_provider_no_transcript():
    """Test OpenAI provider with no transcript"""
    provider = OpenAIProvider("test_key")
    result = provider.evaluate_healthcare_video(None, "test_id")
    assert result["DISCERN Score"] is None
    assert "No transcript" in result["Evaluation Notes"]

def test_parse_evaluation_response():
    """Test parsing evaluation response"""
    from src.healthvidmetrics.ai_providers import _parse_evaluation_response
    
    response = """
    DISCERN Score: 4
    Global Quality Score: 3
    JAMA Criteria Score: 2
    Evaluation Notes: Good quality healthcare content
    """
    
    result = _parse_evaluation_response(response)
    assert result["DISCERN Score"] == 4
    assert result["Global Quality Score"] == 3
    assert result["JAMA Criteria Score"] == 2
    assert "Good quality" in result["Evaluation Notes"] 