"""Cliente para APIs de visão compatíveis com OpenAI."""
from __future__ import annotations

import base64
import os
from dataclasses import dataclass

from .prompt import SYSTEM_PROMPT, build_user_prompt
from .ticket import Ticket, parse_ticket


@dataclass
class Settings:
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            base_url=os.getenv("OPENAI_BASE_URL", cls.base_url).strip() or cls.base_url,
            model=os.getenv("PRINTFIX_MODEL", cls.model).strip() or cls.model,
        )

    @property
    def demo_mode(self) -> bool:
        return not self.api_key


def image_to_data_url(data: bytes, mime: str = "image/png") -> str:
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def build_messages(image: bytes, mime: str, contexto: str = "") -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": [
            {"type": "text", "text": build_user_prompt(contexto)},
            {"type": "image_url", "image_url": {"url": image_to_data_url(image, mime)}},
        ]},
    ]


class PrintFixClient:
    def __init__(self, settings: Settings | None = None, client=None):
        self.settings = settings or Settings.from_env()
        self._client = client

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.settings.api_key, base_url=self.settings.base_url)
        return self._client

    def analyze(self, image: bytes, mime: str = "image/png", contexto: str = "") -> Ticket:
        resp = self._get_client().chat.completions.create(
            model=self.settings.model,
            messages=build_messages(image, mime, contexto),
            temperature=0.2,
        )
        return parse_ticket(resp.choices[0].message.content or "")
