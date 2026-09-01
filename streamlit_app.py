"""
Manual do Núcleo de Isenção de IRPF — Dutra Bitencourt Advocacia
App de acesso interno. Protege o manual com senha e serve sempre a versão
mais recente do arquivo manual.html que estiver no repositório.
"""

import datetime as dt
import pathlib

import streamlit as st

ARQUIVO = pathlib.Path(__file__).parent / "manual.html"
ALTURA = 1500          # altura do quadro do manual, em pixels
MAX_TENTATIVAS = 5     # tentativas de senha antes de bloquear a sessão

st.set_page_config(
    page_title="Manual do Núcleo de Isenção",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# tira o cabeçalho, o rodapé e as margens do Streamlit, para o manual ocupar a tela
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding: 0.4rem 0.6rem 0 0.6rem; max-width: 100%;}
      .stAppDeployButton {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)


def senha_correta() -> str:
    """Lê a senha dos secrets. Sem secret configurado, o app não abre."""
    return st.secrets.get("SENHA", "")


@st.cache_data(show_spinner=False)
def carregar_manual(mtime: float) -> str:
    """Lê o HTML. O mtime entra na assinatura para o cache cair quando o arquivo muda."""
    return ARQUIVO.read_text(encoding="utf-8")


def tela_de_login() -> None:
    esquerda, meio, direita = st.columns([1, 1.1, 1])
    with meio:
        st.write("")
        st.write("")
        st.markdown(
            "<p style='color:#2E6DA4;font-size:13px;letter-spacing:.08em;margin-bottom:2px'>"
            "DUTRA BITENCOURT ADVOCACIA</p>"
            "<h2 style='margin:0 0 4px 0;color:#0E2A47'>Manual do Núcleo de Isenção</h2>"
            "<p style='color:#5C6C7C;margin:0 0 18px 0'>Material interno. Informe a senha para acessar.</p>",
            unsafe_allow_html=True,
        )

        if st.session_state.get("tentativas", 0) >= MAX_TENTATIVAS:
            st.error("Muitas tentativas. Feche a aba e abra novamente.")
            st.stop()

        with st.form("acesso"):
            senha = st.text_input("Senha", type="password", label_visibility="collapsed",
                                  placeholder="Senha de acesso")
            enviar = st.form_submit_button("Entrar", use_container_width=True)

        if enviar:
            if not senha_correta():
                st.error("O app está sem senha configurada. Avise a supervisão.")
            elif senha == senha_correta():
                st.session_state["ok"] = True
                st.session_state["tentativas"] = 0
                st.rerun()
            else:
                st.session_state["tentativas"] = st.session_state.get("tentativas", 0) + 1
                restantes = MAX_TENTATIVAS - st.session_state["tentativas"]
                st.error(f"Senha incorreta. Tentativas restantes: {restantes}.")

        st.caption(
            "Documento de circulação interna. Contém links de pastas e planilhas com dado "
            "de cliente: não compartilhe a senha nem o conteúdo fora do escritório."
        )


def tela_do_manual() -> None:
    if not ARQUIVO.exists():
        st.error("Arquivo manual.html não encontrado no repositório.")
        st.stop()

    atualizado = dt.datetime.fromtimestamp(ARQUIVO.stat().st_mtime).strftime("%d/%m/%Y")

    with st.sidebar:
        st.markdown("### Manual do Núcleo de Isenção")
        st.caption(f"Versão publicada em {atualizado}.")
        st.download_button(
            "Baixar o manual",
            data=carregar_manual(ARQUIVO.stat().st_mtime),
            file_name="MANUAL_ISENCAO_INTERATIVO.html",
            mime="text/html",
            use_container_width=True,
        )
        if st.button("Sair", use_container_width=True):
            st.session_state["ok"] = False
            st.rerun()
        st.caption(
            "A busca, os atalhos e os links funcionam normalmente dentro do quadro. "
            "Use Ctrl+K para ir direto à busca."
        )

    st.components.v1.html(
        carregar_manual(ARQUIVO.stat().st_mtime),
        height=ALTURA,
        scrolling=True,
    )


if st.session_state.get("ok"):
    tela_do_manual()
else:
    tela_de_login()
