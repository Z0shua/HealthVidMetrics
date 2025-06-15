import os
from dotenv import load_dotenv

def load_api_keys():
    load_dotenv()
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    return youtube_api_key, openai_api_key 