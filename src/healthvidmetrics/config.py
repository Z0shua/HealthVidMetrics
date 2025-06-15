import os
from dotenv import load_dotenv

def load_api_keys():
    """Load all API keys from environment variables"""
    load_dotenv()
    
    return {
        'youtube': os.getenv('YOUTUBE_API_KEY'),
        'openai': os.getenv('OPENAI_API_KEY'),
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'gemini': os.getenv('GEMINI_API_KEY'),
        'deepseek': os.getenv('DEEPSEEK_API_KEY'),
        'huggingface': os.getenv('HUGGINGFACE_API_KEY')
    }

def get_ai_provider_config(provider_name: str = None):
    """Get configuration for a specific AI provider"""
    api_keys = load_api_keys()
    
    if provider_name:
        return {
            'provider': provider_name,
            'api_key': api_keys.get(provider_name.lower())
        }
    
    # Return first available provider
    for provider, key in api_keys.items():
        if provider != 'youtube' and key:
            return {
                'provider': provider,
                'api_key': key
            }
    
    return None 