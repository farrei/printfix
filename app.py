"""PrintFix - interface web (Streamlit)."""
import streamlit as st
from dotenv import load_dotenv

from printfix.client import PrintFixClient, Settings
from printfix.demo import SAMPLES, demo_ticket

load_dotenv()
st.set_page_config(page_title="PrintFix", page_icon="🛠️", layout="centered")
st.title("🛠️ PrintFix")
st.caption("Envie o print do erro. A IA devolve o chamado pronto, com diagnóstico e solução.")

settings = Settings.from_env()
if settings.demo_mode:
    st.info("Modo demo: nenhuma OPENAI_API_KEY configurada. Escolha um exemplo abaixo.")
    exemplo = st.selectbox("Exemplo de erro", list(SAMPLES))

arquivo = st.file_uploader("Print do erro", type=["png", "jpg", "jpeg", "webp"])
contexto = st.text_area("Contexto (opcional)", placeholder="Ex.: começou depois da atualização de ontem")
if arquivo:
    st.image(arquivo, use_container_width=True)

if st.button("Gerar chamado", type="primary", disabled=not (arquivo or settings.demo_mode)):
    try:
        if settings.demo_mode:
            ticket = demo_ticket(exemplo)
        else:
            with st.spinner("Analisando o print..."):
                ticket = PrintFixClient(settings).analyze(arquivo.getvalue(), arquivo.type or "image/png", contexto)
        md = ticket.to_markdown()
        st.markdown(md)
        st.download_button("Baixar chamado (.md)", md, file_name="chamado.md")
        with st.expander("JSON"):
            st.json(ticket.model_dump(mode="json"))
    except Exception as e:  # noqa: BLE001
        st.error(f"Não foi possível gerar o chamado: {e}")
