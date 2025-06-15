import re
from typing import Optional
from .ai_providers import create_ai_provider, AIProvider

def evaluate_healthcare_video(transcript: str, video_id: str, 
                            provider_name: str = "openai", 
                            api_key: Optional[str] = None,
                            model: Optional[str] = None) -> dict:
    """
    Evaluate healthcare video quality using specified AI provider
    
    Args:
        transcript: Video transcript text
        video_id: YouTube video ID
        provider_name: AI provider name (openai, anthropic, gemini, deepseek, huggingface)
        api_key: API key for the provider
        model: Model name for the provider (optional)
    
    Returns:
        Dictionary with evaluation scores and notes
    """
    if transcript is None:
        return {
            "DISCERN Score": None,
            "Global Quality Score": None,
            "JAMA Criteria Score": None,
            "Evaluation Notes": "No transcript available for evaluation"
        }
    
    try:
        provider = create_ai_provider(provider_name, api_key, model)
        return provider.evaluate_healthcare_video(transcript, video_id)
    except Exception as e:
        return {
            "DISCERN Score": None,
            "Global Quality Score": None,
            "JAMA Criteria Score": None,
            "Evaluation Notes": f"Evaluation failed: {str(e)}"
        }

# Legacy function for backward compatibility
def evaluate_healthcare_video_openai(transcript, video_id, openai_api_key=None):
    """Legacy function that uses OpenAI specifically"""
    return evaluate_healthcare_video(transcript, video_id, "openai", openai_api_key) 