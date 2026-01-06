import streamlit as st
import os
from pathlib import Path
from dimob_utils import analisar_dimob

# Configuração básica da página
st.set_page_config(
    page_title="Analisador DIMOB",
    page_icon="📄",
    layout="centered"
)

# Autenticação simples por senha
def verificar_senha():
    """Verifica se o usuário está autenticado"""
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        # Senha deve ser definida via variável de ambiente
        # No Railway: Variables > New Variable > DIMOB_SENHA=sua_senha_aqui
        # Localmente: export DIMOB_SENHA=sua_senha_aqui
        senha_correta = None
        
        # Tentar obter do Streamlit Secrets (produção)
        try:
            if hasattr(st, 'secrets') and 'DIMOB_SENHA' in st.secrets:
                senha_correta = st.secrets['DIMOB_SENHA']
        except:
            pass
        
        # Fallback para variável de ambiente (sem senha padrão em produção)
        if not senha_correta:
            senha_correta = os.getenv('DIMOB_SENHA')
        
        # Verificar se senha foi configurada
        if not senha_correta:
            st.title("🔒 Acesso Restrito")
            st.error("⚠️ **Senha não configurada!**")
            st.warning(
                "Configure a variável de ambiente `DIMOB_SENHA` para acessar a aplicação.\n\n"
                "**No Railway:** Vá em Variables e adicione `DIMOB_SENHA=sua_senha_aqui`"
            )
            st.stop()
        
        st.title("🔒 Acesso Restrito")
        st.warning("Esta aplicação é privada. Digite a senha para continuar.")
        
        senha = st.text_input("Senha:", type="password", key="senha_input")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Entrar"):
                if senha == senha_correta:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta!")
        
        st.stop()
    
    return True

# Verificar autenticação antes de mostrar o conteúdo
verificar_senha()

# CSS para destacar o card de R02 (imóveis)
st.markdown(
    """
    <style>
    .destaque-metric {
        border: 2px solid #ffffff55;  /* borda suave (boa no tema escuro/claro) */
        border-radius: 10px;
        padding: 10px 16px;
        margin-top: 4px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📄 Analisador DIMOB")
st.write("Carregue um arquivo `.txt` da DIMOB e veja a contagem de registros.")


uploaded_file = st.file_uploader(
    "Selecione o arquivo DIMOB (.txt)",
    type=["txt"],
    help="Arquivo gerado pelo sistema para envio da DIMOB."
)

if uploaded_file is not None:
    # Lê o conteúdo como texto (latin-1 costuma funcionar bem para arquivos fiscais)
    bytes_data = uploaded_file.read()
    try:
        conteudo = bytes_data.decode("latin-1", errors="ignore")
    except Exception:
        conteudo = bytes_data.decode(errors="ignore")

    total, r01, r02, outros = analisar_dimob(conteudo)

    st.subheader("Resumo do arquivo")
    st.write(f"**Arquivo:** `{uploaded_file.name}`")

    st.markdown("---")

    st.write("### Contagem de registros")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total de linhas (válidas)", total)
        st.metric("Registros R01 (declarante)", r01)

    with col2:
        # Destaque visual para o R02 (imóveis)
        st.markdown('<div class="destaque-metric">', unsafe_allow_html=True)
        st.metric("Registros R02 (imóveis)", r02)
        st.markdown('</div>', unsafe_allow_html=True)

        st.metric("Outros registros/linhas", outros)

    st.markdown("---")
    st.caption(
        "Obs.: 'Outros' = linhas que não começam com R01 nem R02, "
        "desconsiderando linhas totalmente em branco."
    )

else:
    st.info("👆 Envie um arquivo DIMOB `.txt` para começar.")
