from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter


@dataclass
class ModelResponse:
    text: str
    tokens_in: int
    tokens_out: int
    latency_ms: float


class BaseModel:
    def generate(self, prompt: str) -> ModelResponse:  # interface
        raise NotImplementedError


class StubModel(BaseModel):
    """
    Offline, deterministic model for CI. Answers come from data/answers.json.
    If a prompt isn't found, it returns an echo string.
    """

    def __init__(self, answers_path: Path | None = None):
        self.answers: dict[str, str] = {}
        if answers_path and answers_path.exists():
            with answers_path.open("r", encoding="utf-8") as f:
                self.answers = json.load(f)

    @staticmethod
    def _token_estimate(s: str) -> int:
        # Naive token estimator: ~4 chars per token.
        return max(1, len(s) // 4)

    def generate(self, prompt: str) -> ModelResponse:
        start = perf_counter()

        answer = self.answers.get(prompt)
        if answer is None:
            p = prompt.strip().lower()
            if p == "what is 2+2?":
                answer = "4"
            elif "capital of france" in p:
                answer = "Paris"
            else:
                answer = f"Echo: {prompt}"

        latency_ms = (perf_counter() - start) * 1000.0
        tokens_in = self._token_estimate(prompt)
        tokens_out = self._token_estimate(answer)
        return ModelResponse(answer, tokens_in, tokens_out, latency_ms)
