import streamlit as st
from pathlib import Path
from dimob_utils import analisar_dimob

# Configuração básica da página
st.set_page_config(
    page_title="Analisador DIMOB",
    page_icon="📄",
    layout="centered"
)

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
