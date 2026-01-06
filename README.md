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

**Para produção (Render):**
Configure nas variáveis de ambiente do Render (veja seção Deploy abaixo).

⚠️ **IMPORTANTE**: 
- Nunca commite senhas no código ou no Git
- Use variáveis de ambiente sempre
- A senha é obrigatória - a aplicação não funcionará sem ela

## 🌐 Deploy no Render

Este projeto está configurado para deploy no **Render** com Docker.

### Passo a passo:

1. **Criar conta no Render**
   - Acesse [render.com](https://render.com)
   - Faça login com sua conta GitHub

2. **Criar novo Web Service**
   - No dashboard, clique em "New +"
   - Selecione "Web Service"
   - Conecte seu repositório GitHub
   - Escolha o repositório `dimob-analyzer`

3. **Configurar o serviço**
   - **Name**: `dimob-analyzer` (ou o nome que preferir)
   - **Region**: Escolha a região mais próxima (ex: `Oregon (US West)`)
   - **Branch**: `main` (ou `master`)
   - **Runtime**: `Docker` (o Render detectará o Dockerfile automaticamente)
   - **Plan**: `Free` (ou escolha um plano pago)

4. **Configurar variáveis de ambiente**
   - Role até a seção "Environment Variables"
   - Clique em "Add Environment Variable"
   - Adicione:
     ```
     Key: DIMOB_SENHA
     Value: sua_senha_segura_aqui
     ```
   - Clique em "Save Changes"

5. **Deploy**
   - Clique em "Create Web Service"
   - O Render iniciará o build e deploy automaticamente
   - Aguarde alguns minutos (primeiro deploy pode levar 5-10 minutos)

6. **Acessar aplicação**
   - Após o deploy, o Render fornecerá uma URL pública
   - A aplicação estará disponível em: `https://dimob-analyzer.onrender.com` (ou URL customizada)
   - Você pode configurar um domínio customizado nas configurações

### Opção alternativa (sem Docker):

Se preferir usar buildpacks ao invés de Docker:

1. Nas configurações do serviço, mude:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### Configurações importantes:

- **Porta**: Render define automaticamente a variável `PORT` (não precisa configurar)
- **Senha**: **OBRIGATÓRIO** configurar `DIMOB_SENHA` nas variáveis de ambiente
- **HTTPS**: Automático no Render
- **Redeploy**: Automático a cada push no branch conectado
- **Sleep mode**: No plano gratuito, o serviço "dorme" após 15 minutos de inatividade (primeiro acesso pode ser lento)

### Troubleshooting:

- **Erro "Senha não configurada"**: Verifique se a variável `DIMOB_SENHA` está configurada no Render
- **Build falha**: Verifique os logs no Render para ver o erro específico
- **Aplicação não inicia**: Verifique se a porta está configurada corretamente (Render faz isso automaticamente)
- **Timeout no primeiro acesso**: Normal no plano gratuito - o serviço "acorda" após alguns segundos

## 📝 Estrutura do Projeto

```
dimob-analyzer/
├── app.py              # Aplicação principal Streamlit
├── dimob_utils.py      # Funções de análise DIMOB
├── requirements.txt    # Dependências Python
├── Dockerfile          # Configuração Docker para Render/Railway
├── .dockerignore       # Arquivos ignorados no build Docker
├── render.yaml         # Configurações do Render (opcional)
├── start.sh            # Script de inicialização (alternativa)
├── railway.json        # Configurações do Railway (se usar Railway)
└── README.md          # Este arquivo
```

## 📄 Licença

Este projeto é de uso pessoal.

