from types import SimpleNamespace
from printfix.client import PrintFixClient, Settings, build_messages, image_to_data_url

def test_settings_env(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert Settings.from_env().demo_mode
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    monkeypatch.setenv("PRINTFIX_MODEL", "m")
    s = Settings.from_env()
    assert not s.demo_mode and s.model == "m"

def test_data_url():
    assert image_to_data_url(b"hi", "image/jpeg") == "data:image/jpeg;base64,aGk="

def test_messages_include_image_and_context():
    msgs = build_messages(b"x", "image/png", "depois do update")
    assert msgs[0]["role"] == "system"
    assert "depois do update" in msgs[1]["content"][0]["text"]
    assert msgs[1]["content"][1]["image_url"]["url"].startswith("data:image/png")

class FakeCompletions:
    def create(self, **kw):
        self.kw = kw
        c = '{"titulo":"Spooler","categoria":"Impressora","prioridade":"Baixa","diagnostico":"ok ok","passos":["reiniciar"],"quando_escalar":"se falhar"}'
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=c))])

def test_analyze_with_fake_client():
    comp = FakeCompletions()
    fake = SimpleNamespace(chat=SimpleNamespace(completions=comp))
    t = PrintFixClient(Settings(api_key="k", model="vision"), client=fake).analyze(b"img")
    assert t.titulo == "Spooler" and comp.kw["model"] == "vision"
