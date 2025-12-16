# parser_module/adapters/llm_adapter.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

class YandexGptAdapter:
    def __init__(self, api_key: str, model_uri: str, timeout_s: int = 30) -> None:
        self.api_key = api_key
        self.model_uri = model_uri
        self.timeout_s = timeout_s
        self.completion_url: str = (
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        )
        
    def complete(self, prompt: str) -> str:
        payload: Dict[str, Any] = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": "2000",
            },
            "messages": [{"role": "user", "text": prompt}],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}",
        }

        r = requests.post(self.completion_url, headers=headers, json=payload, timeout=self.timeout_s)
        r.raise_for_status()
        data = r.json()
        return data["result"]["alternatives"][0]["message"]["text"]
