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

## 🔒 Segurança

A aplicação possui **autenticação por senha** para proteger seus dados. 

### Configurar Senha

A senha deve ser configurada via **variável de ambiente** `DIMOB_SENHA`. Nunca commite senhas no código!

**Para desenvolvimento local:**
```bash
export DIMOB_SENHA=sua_senha_segura_aqui
streamlit run app.py
```

**Para produção (Railway):**
Configure nas variáveis de ambiente do Railway (veja seção Deploy abaixo).

⚠️ **IMPORTANTE**: 
- Nunca commite senhas no código ou no Git
- Use variáveis de ambiente sempre
- A senha é obrigatória - a aplicação não funcionará sem ela

## 🌐 Deploy no Railway

Este projeto está configurado para deploy no **Railway** com Docker.

### Passo a passo:

1. **Criar conta no Railway**
   - Acesse [railway.app](https://railway.app)
   - Faça login com sua conta GitHub

2. **Criar novo projeto**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório `dimob-analyzer`

3. **Configurar variáveis de ambiente**
   - Vá na aba "Variables" do seu serviço
   - Clique em "New Variable"
   - Adicione:
     ```
     Nome: DIMOB_SENHA
     Valor: sua_senha_segura_aqui
     ```
   - Clique em "Add"

4. **Deploy automático**
   - O Railway detectará o `Dockerfile` automaticamente
   - O build e deploy iniciarão automaticamente
   - Aguarde alguns minutos para o processo completar

5. **Acessar aplicação**
   - Após o deploy, o Railway fornecerá uma URL pública
   - A aplicação estará disponível em: `https://seu-projeto.up.railway.app`
   - Você pode configurar um domínio customizado nas configurações

### Configurações importantes:

- **Porta**: Railway define automaticamente a variável `PORT` (não precisa configurar)
- **Senha**: **OBRIGATÓRIO** configurar `DIMOB_SENHA` nas variáveis de ambiente
- **HTTPS**: Automático no Railway
- **Redeploy**: Automático a cada push no branch conectado (geralmente `main` ou `master`)

### Troubleshooting:

- **Erro "Senha não configurada"**: Verifique se a variável `DIMOB_SENHA` está configurada no Railway
- **Build falha**: Verifique os logs no Railway para ver o erro específico
- **Aplicação não inicia**: Verifique se a porta está configurada corretamente (Railway faz isso automaticamente)

## 📝 Estrutura do Projeto

```
dimob-analyzer/
├── app.py              # Aplicação principal Streamlit
├── dimob_utils.py      # Funções de análise DIMOB
├── requirements.txt    # Dependências Python
├── Dockerfile          # Configuração Docker para Railway
├── .dockerignore       # Arquivos ignorados no build Docker
├── railway.json        # Configurações do Railway
└── README.md          # Este arquivo
```

## 📄 Licença

Este projeto é de uso pessoal.

