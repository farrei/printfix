"""Modelo de chamado (ticket) de helpdesk."""
from __future__ import annotations

import json
import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Categoria(str, Enum):
    WINDOWS = "Windows"
    IMPRESSORA = "Impressora"
    EMAIL = "E-mail/Outlook"
    REDE = "Rede"
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    ACESSO = "Acesso/Senha"
    OUTRO = "Outro"


class Prioridade(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    CRITICA = "Crítica"


class Ticket(BaseModel):
    titulo: str = Field(min_length=3, max_length=120)
    categoria: Categoria = Categoria.OUTRO
    prioridade: Prioridade = Prioridade.MEDIA
    diagnostico: str = Field(min_length=3)
    passos: list[str] = Field(min_length=1)
    quando_escalar: str = Field(min_length=3)
    confianca: float = Field(default=0.5, ge=0.0, le=1.0)

    @field_validator("categoria", mode="before")
    @classmethod
    def _cat(cls, v):
        if isinstance(v, Categoria):
            return v
        for c in Categoria:
            if str(v).strip().lower() == c.value.lower():
                return c
        return Categoria.OUTRO

    @field_validator("prioridade", mode="before")
    @classmethod
    def _prio(cls, v):
        if isinstance(v, Prioridade):
            return v
        aliases = {"media": "Média", "critica": "Crítica"}
        s = str(v).strip()
        s = aliases.get(s.lower(), s)
        for p in Prioridade:
            if s.lower() == p.value.lower():
                return p
        return Prioridade.MEDIA

    def to_markdown(self) -> str:
        passos = "\n".join(f"{i}. {p}" for i, p in enumerate(self.passos, 1))
        return (
            f"## 🎫 {self.titulo}\n\n"
            f"**Categoria:** {self.categoria.value}  \n"
            f"**Prioridade:** {self.prioridade.value}  \n"
            f"**Confiança da IA:** {self.confianca:.0%}\n\n"
            f"### Diagnóstico\n{self.diagnostico}\n\n"
            f"### Passos para resolver\n{passos}\n\n"
            f"### Quando escalar\n{self.quando_escalar}\n"
        )


def parse_ticket(raw: str) -> Ticket:
    """Extrai JSON da resposta do modelo (aceita blocos ```json```)."""
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise ValueError("Resposta do modelo não contém JSON.")
    return Ticket.model_validate(json.loads(m.group(0)))
