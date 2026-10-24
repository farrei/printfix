import pytest
from printfix.ticket import Categoria, Prioridade, Ticket, parse_ticket
from printfix.demo import SAMPLES, demo_ticket

RAW = '```json\n{"titulo":"Erro X","categoria":"impressora","prioridade":"critica","diagnostico":"abc","passos":["a"],"quando_escalar":"nunca","confianca":0.9}\n```'

def test_parse_code_block_and_normalize():
    t = parse_ticket(RAW)
    assert t.categoria is Categoria.IMPRESSORA
    assert t.prioridade is Prioridade.CRITICA

def test_unknown_values_fallback():
    t = Ticket(titulo="abc", categoria="xyz", prioridade="??", diagnostico="abc", passos=["x"], quando_escalar="abc")
    assert t.categoria is Categoria.OUTRO and t.prioridade is Prioridade.MEDIA

def test_no_json_raises():
    with pytest.raises(ValueError):
        parse_ticket("sem json aqui")

def test_empty_steps_invalid():
    with pytest.raises(Exception):
        Ticket(titulo="abc", diagnostico="abc", passos=[], quando_escalar="abc")

def test_markdown_has_sections():
    md = demo_ticket().to_markdown()
    for s in ("Diagnóstico", "Passos para resolver", "Quando escalar", "1."):
        assert s in md

@pytest.mark.parametrize("nome", list(SAMPLES))
def test_all_samples_valid(nome):
    assert demo_ticket(nome).passos
