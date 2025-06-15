"""
AI Provider abstraction for HealthVidMetrics
Supports multiple AI providers: OpenAI, Anthropic, Google Gemini, DeepSeek, Hugging Face, etc.
"""

import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import openai
import anthropic
import google.generativeai as genai
import requests
from huggingface_hub import InferenceClient

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    # Standard evaluation prompt template
    EVALUATION_PROMPT_TEMPLATE = """
    You are a healthcare content quality evaluator. Analyze the following YouTube video transcript and provide scores based on established healthcare quality metrics.

    TRANSCRIPT:
    {transcript}

    Please evaluate this healthcare video content and provide the following scores:

    1. DISCERN Score (1-5): Rate the reliability and quality of health information
       - 1: Very poor quality, potentially harmful
       - 2: Poor quality, unreliable information
       - 3: Moderate quality, some concerns
       - 4: Good quality, generally reliable
       - 5: Excellent quality, highly reliable

    2. Global Quality Score (1-5): Overall educational and informational quality
       - 1: Very poor overall quality
       - 2: Poor overall quality
       - 3: Moderate overall quality
       - 4: Good overall quality
       - 5: Excellent overall quality

    3. JAMA Criteria Score (0-4): Based on JAMA benchmark criteria (Authorship, Attribution, Currency, Disclosure)
       - 0: Meets none of the criteria
       - 1: Meets 1 criterion
       - 2: Meets 2 criteria
       - 3: Meets 3 criteria
       - 4: Meets all 4 criteria

    Provide your response in this exact format:
    DISCERN Score: [number]
    Global Quality Score: [number]
    JAMA Criteria Score: [number]
    Evaluation Notes: [brief explanation of scores]
    """
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model
        self._setup_client()
    
    @abstractmethod
    def _setup_client(self):
        """Setup the AI client with API key"""
        pass
    
    @abstractmethod
    def _call_api(self, prompt: str) -> str:
        """Make API call to the AI provider"""
        pass
    
    def evaluate_healthcare_video(self, transcript: str, video_id: str) -> Dict[str, Any]:
        """Evaluate healthcare video quality using standardized prompt"""
        if transcript is None:
            return self._get_empty_result("No transcript available for evaluation")
        
        # Limit transcript length for API efficiency
        limited_transcript = transcript[:4000]
        prompt = self.EVALUATION_PROMPT_TEMPLATE.format(transcript=limited_transcript)
        
        try:
            evaluation = self._call_api(prompt)
            return self._parse_evaluation_response(evaluation)
        except Exception as e:
            return self._get_empty_result(f"Evaluation failed: {str(e)}")
    
    def _parse_evaluation_response(self, evaluation: str) -> Dict[str, Any]:
        """Parse evaluation response from any AI provider"""
        discern_match = re.search(r"DISCERN Score:\s*(\d)", evaluation)
        global_quality_match = re.search(r"Global Quality Score:\s*(\d)", evaluation)
        jama_match = re.search(r"JAMA Criteria Score:\s*(\d)", evaluation)
        notes_match = re.search(r"Evaluation Notes:\s*(.+)", evaluation, re.DOTALL)
        
        return {
            "DISCERN Score": int(discern_match.group(1)) if discern_match else None,
            "Global Quality Score": int(global_quality_match.group(1)) if global_quality_match else None,
            "JAMA Criteria Score": int(jama_match.group(1)) if jama_match else None,
            "Evaluation Notes": notes_match.group(1).strip() if notes_match else "Evaluation completed"
        }
    
    def _get_empty_result(self, notes: str) -> Dict[str, Any]:
        """Get empty result for failed evaluations"""
        return {
            "DISCERN Score": None,
            "Global Quality Score": None,
            "JAMA Criteria Score": None,
            "Evaluation Notes": notes
        }

class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    
    def _setup_client(self):
        openai.api_key = self.api_key
    
    def _call_api(self, prompt: str) -> str:
        model = self.model or "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a healthcare content quality evaluator with expertise in medical information assessment."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

class AnthropicProvider(AIProvider):
    """Anthropic Claude provider"""
    
    def _setup_client(self):
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def _call_api(self, prompt: str) -> str:
        model = self.model or "claude-3-haiku-20240307"
        response = self.client.messages.create(
            model=model,
            max_tokens=300,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class GeminiProvider(AIProvider):
    """Google Gemini provider"""
    
    def _setup_client(self):
        genai.configure(api_key=self.api_key)
        model = self.model or "gemini-1.5-flash"
        self.client = genai.GenerativeModel(model)
    
    def _call_api(self, prompt: str) -> str:
        response = self.client.generate_content(prompt)
        return response.text

class DeepSeekProvider(AIProvider):
    """DeepSeek provider"""
    
    def _setup_client(self):
        self.base_url = "https://api.deepseek.com/v1"
    
    def _call_api(self, prompt: str) -> str:
        model = self.model or "deepseek-chat"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.3
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]

class HuggingFaceProvider(AIProvider):
    """Hugging Face Inference API provider"""
    
    def _setup_client(self):
        model = self.model or "meta-llama/Llama-2-7b-chat-hf"
        self.client = InferenceClient(model=model, token=self.api_key)
    
    def _call_api(self, prompt: str) -> str:
        response = self.client.text_generation(
            prompt,
            max_new_tokens=300,
            temperature=0.3,
            do_sample=True
        )
        return response

# Provider factory
def create_ai_provider(provider_name: str, api_key: str, model: Optional[str] = None) -> AIProvider:
    """Create an AI provider instance based on provider name"""
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "deepseek": DeepSeekProvider,
        "huggingface": HuggingFaceProvider
    }
    
    if provider_name.lower() not in providers:
        raise ValueError(f"Unsupported provider: {provider_name}. Supported providers: {list(providers.keys())}")
    
    provider_class = providers[provider_name.lower()]
    return provider_class(api_key, model) 