# PrintFix

[![CI](https://github.com/farrei/printfix/actions/workflows/ci.yml/badge.svg)](https://github.com/farrei/printfix/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

Cole o print de um erro (Windows, impressora, Outlook) e receba um chamado de helpdesk pronto, em português.

## Por que fiz isso
Trabalhando com suporte, percebi que a maior parte do tempo do primeiro atendimento vai em entender o que o usuário está vendo. Chega um "deu erro aqui" com um print, e alguém precisa interpretar, pesquisar e registrar. O PrintFix faz essa primeira leitura: manda o print para um modelo com visão, identifica o erro e a causa provável e devolve um chamado com título, categoria, prioridade, diagnóstico, passos de solução e quando escalar.

## Como funciona
```mermaid
flowchart LR
    U[Usuário] -->|print + contexto| UI[Streamlit app.py]
    UI --> C{API key configurada?}
    C -- não --> D[Modo demo<br/>printfix/demo.py]
    C -- sim --> P[Prompt de sistema<br/>printfix/prompt.py]
    P --> API[API de visão compatível<br/>com OpenAI]
    API -->|JSON| V[Validação Pydantic<br/>printfix/ticket.py]
    D --> V
    V --> T[Chamado em Markdown + JSON]
```

| Módulo | Responsabilidade |
|---|---|
| `printfix/prompt.py` | Prompt do analista N1/N2 com o formato JSON exigido |
| `printfix/client.py` | Configuração via env vars e chamada à API de visão |
| `printfix/ticket.py` | Modelo `Ticket` (Pydantic), normalização e exportação em Markdown |
| `printfix/demo.py` | Respostas de exemplo para rodar sem chave |
| `app.py` | Interface web |

## Rodando
```bash
git clone https://github.com/farrei/printfix.git && cd printfix
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Sem chave de API o app abre em modo demo, com três casos prontos: impressora offline, Outlook pedindo senha e tela azul. Para usar um modelo de verdade, copie `.env.example` para `.env` e preencha `OPENAI_API_KEY`.

| Variável | Padrão | Descrição |
|---|---|---|
| `OPENAI_API_KEY` | vazio | Chave da API. Vazio = modo demo |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | Qualquer provedor compatível com a API da OpenAI |
| `PRINTFIX_MODEL` | `gpt-4o-mini` | Modelo com suporte a imagem |

## Stack
Python, Streamlit, Pydantic e API compatível com OpenAI (visão). Testes com pytest e CI no GitHub Actions (Python 3.10 a 3.12).

## Testes
```bash
pytest -q
```
São 12 testes, todos passando. Eles usam um cliente falso, então rodam sem chave e sem internet.

## Próximos passos
- Abrir o chamado direto no GLPI ou Jira Service Management
- Base de conhecimento local com soluções já usadas pela equipe
- OCR offline como alternativa
- Histórico de chamados e métricas por tipo de erro

## English
PrintFix turns a screenshot of an IT error into a ready-to-file helpdesk ticket (title, category, priority, diagnosis, fix steps, escalation criteria) in Brazilian Portuguese, using any OpenAI-compatible vision model. Python, Streamlit, Pydantic; demo mode without an API key, 12 tests, CI.

## Autor
Rafael Verissimo, São Paulo. Estudante de Análise e Desenvolvimento de Sistemas (UNINTER), com experiência em suporte de TI. [github.com/farrei](https://github.com/farrei)

Licença [MIT](LICENSE).
