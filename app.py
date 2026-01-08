import csv
from typing import Optional
import streamlit as st
import os
import pandas as pd
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
        # No Render: Environment Variables > Add > DIMOB_SENHA=sua_senha_aqui
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
                "**No Render:** Vá em Environment Variables e adicione `DIMOB_SENHA=sua_senha_aqui`"
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


def _detectar_delimitador(linha: str) -> str:
    candidatos = ["|", ";", "\t", ","]
    melhor = ""
    max_contagem = 0
    for candidato in candidatos:
        contagem = linha.count(candidato)
        if contagem > max_contagem:
            max_contagem = contagem
            melhor = candidato
    return melhor if max_contagem > 0 else ""


def _normalizar_colunas(colunas):
    colunas_limpa = []
    contadores = {}
    for coluna in colunas:
        nome = coluna.strip().strip('"')
        if not nome:
            nome = "col"
        if nome in contadores:
            contadores[nome] += 1
            nome = f"{nome}_{contadores[nome]}"
        else:
            contadores[nome] = 1
        colunas_limpa.append(nome)
    return colunas_limpa


def _formatar_doc(doc: str) -> str:
    digitos = "".join(ch for ch in doc if ch.isdigit())
    if len(digitos) == 11:
        return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"
    if len(digitos) == 14:
        return f"{digitos[:2]}.{digitos[2:5]}.{digitos[5:8]}/{digitos[8:12]}-{digitos[12:]}"
    return doc.strip()


def _formatar_data(data: str) -> str:
    data = "".join(ch for ch in data if ch.isdigit())
    if len(data) == 8:
        return f"{data[:2]}/{data[2:4]}/{data[4:]}"
    return data


def _formatar_moeda_centavos(valor_centavos: int) -> str:
    valor = valor_centavos / 100
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def _parse_centavos(valor: str) -> int:
    digitos = "".join(ch for ch in valor if ch.isdigit())
    return int(digitos) if digitos else 0


def _extrair_valores_r02(segmento: str) -> list:
    valores = []
    for i in range(0, len(segmento), 14):
        chunk = segmento[i : i + 14]
        if len(chunk) < 14:
            break
        valores.append(_parse_centavos(chunk))
    while len(valores) < 36:
        valores.append(0)
    return valores[:36]


def _totais_r02(valores: list) -> tuple:
    blocos = [
        sum(valores[0:12]),
        sum(valores[12:24]),
        sum(valores[24:36]),
    ]
    blocos_com_valor = [(indice, total) for indice, total in enumerate(blocos) if total > 0]
    if not blocos_com_valor:
        return 0, 0
    if len(blocos_com_valor) == 1:
        return blocos_com_valor[0][1], 0
    blocos_ordenados = sorted(blocos_com_valor, key=lambda item: item[1], reverse=True)
    return blocos_ordenados[0][1], blocos_ordenados[1][1]


def _parse_r02_linha(linha: str, numero_linha: int) -> dict:
    linha = linha.rstrip("\n")
    if len(linha) < 788:
        linha = linha.ljust(788)

    nome1 = linha[40:100].strip()
    doc1 = _formatar_doc(linha[100:114])
    nome2 = linha[114:174].strip()
    codigo_imovel = linha[174:179].strip()
    data = _formatar_data(linha[180:188])
    valores = _extrair_valores_r02(linha[188:692])
    valor_total, comissao_total = _totais_r02(valores)
    endereco = linha[692:788].strip()

    return {
        "linha": numero_linha,
        "locador_nome": nome1,
        "locador_doc": doc1,
        "locatario_nome": nome2,
        "codigo_imovel": codigo_imovel,
        "data": data,
        "endereco": endereco,
        "valor_total": valor_total,
        "comissao_total": comissao_total,
    }


def extrair_tabela_r02(conteudo: str) -> pd.DataFrame:
    """Desmembra registros R02 em uma tabela detalhada."""
    rows = []
    for numero_linha, linha in enumerate(conteudo.splitlines(), start=1):
        if not linha.startswith("R02"):
            continue
        dados = _parse_r02_linha(linha, numero_linha)

        locador = dados["locador_nome"]
        if dados["locador_doc"]:
            locador = f"{locador} ({dados['locador_doc']})" if locador else dados["locador_doc"]

        locatario = dados["locatario_nome"]
        if dados["data"]:
            locatario = f"{locatario} - {dados['data']}" if locatario else dados["data"]

        partes_imovel = []
        if dados["codigo_imovel"]:
            partes_imovel.append(dados["codigo_imovel"])
        if dados["endereco"]:
            partes_imovel.append(dados["endereco"])
        imovel = " - ".join(partes_imovel)

        rows.extend(
            [
                {
                    "linha": dados["linha"],
                    "item": "LOCADOR",
                    "descricao": locador,
                    "valor": "",
                    "comissao": "",
                },
                {
                    "linha": dados["linha"],
                    "item": "LOCATARIO",
                    "descricao": locatario,
                    "valor": "",
                    "comissao": "",
                },
                {
                    "linha": dados["linha"],
                    "item": "IMOVEL",
                    "descricao": imovel,
                    "valor": "",
                    "comissao": "",
                },
                {
                    "linha": dados["linha"],
                    "item": "TOTAL",
                    "descricao": "",
                    "valor": _formatar_moeda_centavos(dados["valor_total"]),
                    "comissao": _formatar_moeda_centavos(dados["comissao_total"]),
                },
            ]
        )

    return pd.DataFrame(rows)


def extrair_tabela_txt(conteudo: str) -> pd.DataFrame:
    """Cria uma tabela a partir do cabecalho do TXT DIMOB."""
    linhas = conteudo.splitlines()
    indice_cabecalho = None
    for indice, linha in enumerate(linhas):
        if linha.strip():
            indice_cabecalho = indice
            break

    if indice_cabecalho is None:
        return pd.DataFrame()

    cabecalho_raw = linhas[indice_cabecalho].rstrip("\n")
    delimitador = _detectar_delimitador(cabecalho_raw)

    if not delimitador:
        rows = []
        for numero_linha, linha in enumerate(linhas, start=1):
            linha = linha.rstrip("\n")
            if not linha.strip():
                continue
            tipo = linha[:3] if len(linha) >= 3 else ""
            rows.append({"linha": numero_linha, "tipo": tipo, "conteudo": linha})
        return pd.DataFrame(rows)

    cabecalho = cabecalho_raw.split(delimitador)
    remover_inicio = bool(cabecalho and not cabecalho[0])
    remover_fim = bool(cabecalho and not cabecalho[-1])
    if remover_inicio:
        cabecalho = cabecalho[1:]
    if remover_fim:
        cabecalho = cabecalho[:-1]
    cabecalho = _normalizar_colunas(cabecalho)

    col_linha = "linha"
    if col_linha in cabecalho:
        col_linha = "linha_arquivo"

    rows = []
    for numero_linha, linha in enumerate(linhas[indice_cabecalho + 1 :], start=indice_cabecalho + 2):
        linha = linha.rstrip("\n")
        if not linha.strip():
            continue
        campos = next(csv.reader([linha], delimiter=delimitador))
        if remover_inicio and campos:
            campos = campos[1:]
        if remover_fim and campos:
            campos = campos[:-1]
        if len(campos) < len(cabecalho):
            campos += [""] * (len(cabecalho) - len(campos))
        elif len(campos) > len(cabecalho):
            campos = campos[: len(cabecalho) - 1] + [delimitador.join(campos[len(cabecalho) - 1 :])]

        registro = dict(zip(cabecalho, [campo.strip() for campo in campos]))
        registro[col_linha] = numero_linha
        rows.append(registro)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    if col_linha in df.columns:
        colunas = [col_linha] + [col for col in df.columns if col != col_linha]
        df = df[colunas]
    return df


def abrir_modal_tabela_txt(
    df: pd.DataFrame,
    nome_arquivo: str,
    titulo: Optional[str] = None,
) -> None:
    titulo = titulo or f"Tabela do TXT: {nome_arquivo}"

    if hasattr(st, "dialog"):
        @st.dialog(titulo)
        def _dialog():
            st.dataframe(df, use_container_width=True, height=420)

        _dialog()
    elif hasattr(st, "experimental_dialog"):
        @st.experimental_dialog(titulo)
        def _dialog():
            st.dataframe(df, use_container_width=True, height=420)

        _dialog()
    else:
        st.info("Seu Streamlit não suporta modal. Veja os dados abaixo.")
        st.dataframe(df, use_container_width=True, height=420)

# Verificar autenticação antes de mostrar o conteúdo
verificar_senha()

# CSS para destacar o card de R02 (imóveis)
st.markdown(
    """
    <style>
    .stDialog [role="dialog"] {
        width: 95vw;
        max-width: 1400px;
    }
    .stDialog [data-testid="stDataFrame"] {
        width: 100%;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px 24px;
        margin-top: 8px;
    }
    .metric-card {
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
        background: rgba(148, 163, 184, 0.08);
        box-shadow: 0 6px 16px rgba(2, 6, 23, 0.12);
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        opacity: 0.9;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .metric-card.destaque-card {
        border-color: rgba(34, 197, 94, 0.65);
        box-shadow:
            0 0 0 2px rgba(34, 197, 94, 0.18),
            0 10px 20px rgba(2, 6, 23, 0.16);
        background: linear-gradient(
            135deg,
            rgba(34, 197, 94, 0.08),
            rgba(56, 189, 248, 0.08)
        );
    }
    .metric-card.destaque-card .metric-label,
    .metric-card.destaque-card .metric-value {
        color: #22c55e;
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
    r02_df = extrair_tabela_r02(conteudo)

    resumo_col, botao_col = st.columns([4, 1])
    with resumo_col:
        st.subheader("Resumo do arquivo")
    with botao_col:
        ver_tabela_r02 = st.button("Ver tabela R02", use_container_width=True)

    if ver_tabela_r02:
        if r02_df.empty:
            st.warning("Não foram encontrados registros R02 para detalhar.")
        else:
            abrir_modal_tabela_txt(
                r02_df,
                uploaded_file.name,
                titulo=f"Tabela R02: {uploaded_file.name}",
            )

    st.write(f"**Arquivo:** `{uploaded_file.name}`")

    st.markdown("---")

    st.write("### Contagem de registros")

    st.markdown(
        f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total de linhas (válidas)</div>
                <div class="metric-value">{total}</div>
            </div>
            <div class="metric-card destaque-card">
                <div class="metric-label">Registros R02 (imóveis)</div>
                <div class="metric-value">{r02}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Registros R01 (declarante)</div>
                <div class="metric-value">{r01}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Outros registros/linhas</div>
                <div class="metric-value">{outros}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption(
        "Obs.: 'Outros' = linhas que não começam com R01 nem R02, "
        "desconsiderando linhas totalmente em branco."
    )

else:
    st.info("👆 Envie um arquivo DIMOB `.txt` para começar.")
