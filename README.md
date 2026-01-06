# 📄 Analisador DIMOB

Aplicação web para análise de arquivos DIMOB (Declaração de Informações sobre Movimentação de Bens).

## 🚀 Funcionalidades

- Upload de arquivos DIMOB (.txt)
- Contagem automática de registros:
  - **R01**: Registros de declarante
  - **R02**: Registros de imóveis (destaque visual)
  - **Outros**: Outros tipos de registros

## 📋 Requisitos

- Python 3.8+
- Streamlit
- Pandas

## 🛠️ Instalação Local

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

## 🌐 Deploy

Este projeto está configurado para deploy no **Streamlit Cloud**:

1. Faça push do código para um repositório GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório GitHub
4. Selecione o branch e arquivo principal (`app.py`)
5. Clique em "Deploy"

## 📝 Estrutura do Projeto

```
dimob-analyzer/
├── app.py              # Aplicação principal Streamlit
├── dimob_utils.py      # Funções de análise DIMOB
├── requirements.txt    # Dependências Python
└── README.md          # Este arquivo
```

## 📄 Licença

Este projeto é de uso pessoal.

