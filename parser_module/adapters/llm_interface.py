from __future__ import annotations

from typing import Protocol


class LlmInterface(Protocol):
    def complete(self, prompt: str) -> str:
        pass


