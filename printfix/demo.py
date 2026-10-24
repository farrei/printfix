"""Respostas de exemplo para o modo demo (sem API key)."""
from .ticket import Ticket

SAMPLES: dict[str, dict] = {
    "Impressora offline": {
        "titulo": "Impressora aparece como 'Offline' no Windows",
        "categoria": "Impressora", "prioridade": "Média",
        "diagnostico": "O Windows perdeu comunicação com a impressora. Causas comuns: IP alterado por DHCP, spooler travado ou cabo/Wi-Fi desconectado.",
        "passos": [
            "Verifique se a impressora está ligada e conectada à rede (veja o IP no painel).",
            "Em Configurações > Impressoras, desmarque 'Usar impressora offline'.",
            "Reinicie o serviço Spooler: Win+R > services.msc > Spooler de Impressão > Reiniciar.",
            "Confira se a porta TCP/IP da impressora aponta para o IP atual.",
            "Remova e adicione a impressora novamente, se necessário.",
        ],
        "quando_escalar": "Se outros usuários também não imprimem ou a impressora não obtém IP, escalar para Infra/Redes ou fornecedor.",
        "confianca": 0.86,
    },
    "Outlook pedindo senha": {
        "titulo": "Outlook solicita senha repetidamente",
        "categoria": "E-mail/Outlook", "prioridade": "Alta",
        "diagnostico": "Credenciais em cache corrompidas ou senha alterada recentemente; também pode ser falha de autenticação moderna.",
        "passos": [
            "Confirme se o usuário consegue entrar no Outlook Web (OWA) com a mesma senha.",
            "Abra o Gerenciador de Credenciais do Windows e remova entradas de Outlook/Office.",
            "Feche o Outlook, reabra e faça login novamente.",
            "Se persistir, crie um novo perfil em Painel de Controle > Email > Mostrar Perfis.",
        ],
        "quando_escalar": "Se o login falhar também no OWA (conta bloqueada/MFA), escalar para o time de Identidade/M365.",
        "confianca": 0.82,
    },
    "Tela azul (BSOD)": {
        "titulo": "Tela azul com erro IRQL_NOT_LESS_OR_EQUAL",
        "categoria": "Windows", "prioridade": "Alta",
        "diagnostico": "Geralmente causado por driver incompatível ou memória RAM com defeito.",
        "passos": [
            "Anote o código de parada e o arquivo citado (ex.: .sys).",
            "Inicie em Modo Seguro e desinstale drivers instalados recentemente.",
            "Execute o Diagnóstico de Memória do Windows (mdsched.exe).",
            "Rode 'sfc /scannow' e 'DISM /Online /Cleanup-Image /RestoreHealth' como administrador.",
            "Atualize drivers pelo site do fabricante.",
        ],
        "quando_escalar": "Se a tela azul persistir após os testes ou o diagnóstico de memória acusar falha, encaminhar para N2/Hardware.",
        "confianca": 0.74,
    },
}


def demo_ticket(nome: str | None = None) -> Ticket:
    nome = nome if nome in SAMPLES else next(iter(SAMPLES))
    return Ticket.model_validate(SAMPLES[nome])
