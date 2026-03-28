<div align="center">

<br/>

```
████████╗███████╗ ██████╗██╗  ██╗███████╗ ██████╗ ██╗     ██╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔════╝██╔═══██╗██║     ██║   ██║╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
   ██║   █████╗  ██║     ███████║███████╗██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║███████╗
   ██║   ██╔══╝  ██║     ██╔══██║╚════██║██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
   ██║   ███████╗╚██████╗██║  ██║███████║╚██████╔╝███████╗╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║███████║
   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
```

# 🤖 RPA — Automação de Cobrança

**Sistema completo de automação do fluxo financeiro da TechSolutions Ltda.**
Cadastro · Boletos PDF · QR Code PIX · WhatsApp Web · Gmail · Relatórios Excel

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_App-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Selenium](https://img.shields.io/badge/Selenium-RPA-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium-python.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

<br/>

> 🎓 **Avaliação 1 — Linguagem de Programação III**
> Entrega: **27/03** (Grupo 1) · **10/04** (Grupo 2)

<br/>

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar](#-como-executar)
- [Interface Gráfica](#-interface-gráfica-opcional)
- [Banco de Dados](#-banco-de-dados)
- [Exemplos de Saída](#-exemplos-de-saída)
- [Observações Importantes](#️-observações-importantes)
- [Gitignore Recomendado](#-arquivo-gitignore-recomendado)

---

## 🎯 Sobre o Projeto

A **TechSolutions Ltda** é uma empresa de consultoria que realizava todo o processo de cobrança de forma manual: planilhas Excel, boletos digitados um a um e ligações telefônicas para clientes inadimplentes. Esse fluxo gerava erros, retrabalho e perda de tempo.

Este projeto automatiza **100% desse fluxo** usando técnicas de **RPA (Robotic Process Automation)** com Python:

```
📊 Lê Excel  →  🌐 Cadastra no Sistema  →  📄 Gera Boleto PDF  →  📱 WhatsApp  →  📧 E-mail  →  📊 Relatório
```

| Antes (Manual) | Depois (RPA) |
|---|---|
| 2h/dia digitando clientes em planilha | ⚡ Importação automática em segundos |
| Boletos digitados um por um | ⚡ PDFs gerados em lote automaticamente |
| 50 ligações/dia para cobrar clientes | ⚡ WhatsApp automático para todos |
| Sem histórico estruturado | ⚡ Relatório Excel completo com dashboard |

---

## 🏗 Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERFACE GRÁFICA                        │
│                    FreeSimpleGUI (gui.py)                        │
│         [ Web ] [ RPA ] [ PDF ] [ WA ] [ Email ] [ Excel ]      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
       ┌───────────────────────┼──────────────────────┐
       ▼                       ▼                       ▼
┌─────────────┐       ┌────────────────┐      ┌───────────────┐
│  PARTE 1    │       │   PARTE 2      │      │  PARTES 3-4   │
│  Sistema    │◄──────│  Gera PDFs     │─────►│  WhatsApp     │
│  Web Flask  │       │  + QR Code     │      │  + Gmail      │
│  + RPA      │       │                │      │               │
└──────┬──────┘       └────────────────┘      └───────────────┘
       │                                               │
       ▼                                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     SQLite Database                          │
│         tabela: clientes  ←FK→  tabela: faturas             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │    PARTE 5       │
                    │  Relatório Excel │
                    │  + Aba Resumo    │
                    └──────────────────┘
```

---

## 📁 Estrutura de Pastas

```
AV1/
│
├── 📂 1parte_web/                    # Sistema Web
│   ├── 🐍 app.py                     # Servidor Flask (rotas, dashboard)
│   ├── 🐍 database.py                # Conexão e queries SQLite
│   ├── 🗄️  techsolutions.db           # Banco de dados
│   └── 📂 templates/
│       ├── base.html                 # Layout base
│       ├── index.html                # Dashboard principal
│       ├── clientes.html             # Listagem de clientes
│       ├── faturas.html              # Listagem de faturas
│       ├── form_cliente.html         # Formulário de cadastro
│       └── form_fatura.html          # Formulário de fatura
│
├── 📂 parte1_rpa/
│   └── 🐍 rpa_cadastro.py            # Lê Excel e preenche o sistema via Selenium
│
├── 📂 parte2_pdf/
│   └── 🐍 gerar_boletos.py           # Gera boletos PDF + QR Code PIX
│
├── 📂 parte3_whatsapp/
│   └── 🐍 enviar_whatsapp.py         # Envia mensagens via WhatsApp Web
│
├── 📂 parte4_email/
│   └── 🐍 enviar_email.py            # Envia e-mails com boleto anexado (Gmail)
│
├── 📂 parte5_relatorio/
│   └── 🐍 relatorio_excel.py         # Exporta relatório Excel com resumo
│
├── 📂 interface/
│   └── 🐍 gui.py                     # Interface gráfica FreeSimpleGUI ⭐ OPCIONAL
│
├── 📂 dados/
│   ├── 📊 clientes_importar.xlsx     # Planilha de entrada (5+ clientes)
│   ├── 📊 faturas_relatorio.xlsx     # Relatório gerado automaticamente
│   ├── 📄 email_log.txt              # Log de envios de e-mail
│   └── 📄 erros.csv                  # Registro de erros do WhatsApp
│
├── 📂 boletos/                       # PDFs gerados (boleto_cliente001_Nome.pdf)
│
└── 📂 config/
    └── 🔒 .env                       # Variáveis de ambiente (NÃO commitar!)
```

---

## ✨ Funcionalidades

### 🌐 Parte 1 — Sistema Web + RPA de Cadastro `(2,0 pts)`

**Sistema Web (Flask + SQLite)**
- Dashboard com totais de clientes, faturas e pendências
- Formulário de cadastro de clientes (nome, e-mail, telefone, endereço)
- Formulário de emissão de faturas vinculadas ao cliente
- Listagem completa de clientes e faturas
- Banco relacional com chave estrangeira entre as tabelas

**RPA com Selenium**
- Lê planilha Excel com 5+ clientes automaticamente
- Abre Chrome, navega até o sistema web e preenche cada formulário
- Detecta sucesso/falha de cada cadastro
- Atualiza a planilha com a coluna **"Status RPA"**: 🟢 verde = sucesso, 🔴 vermelho = falha

---

### 📄 Parte 2 — Geração de PDF com QR Code `(1,5 pts)`

- Layout profissional com cabeçalho colorido e identidade visual da empresa
- Dados completos: nome do cliente, valor, data de vencimento, número da fatura
- **Código de barras** simulado em formato digitável
- **QR Code PIX** gerado e embutido no PDF — legível por qualquer app bancário
- Geração em lote: 1 PDF por fatura, nomenclatura padronizada (`boleto_cliente001_Nome.pdf`)
- Rodapé com data/hora de geração

---

### 📱 Parte 3 — Envio via WhatsApp Web `(2,5 pts)`

- Selenium abre o WhatsApp Web com aguardo configurável para escanear QR Code
- Mensagem **personalizada** por cliente com nome, valor, vencimento e link do boleto
- Validação do número de telefone antes do envio
- Envio com `pyautogui` (simula tecla Enter)
- Erros registrados automaticamente em `dados/erros.csv`
- Status da fatura atualizado no banco após envio (`enviado` / `falhou`)

---

### 📧 Parte 4 — Envio de E-mail via Gmail

- E-mail em **HTML responsivo** com gradiente, tabela formatada e aviso de vencimento
- Boleto PDF **anexado automaticamente** ao e-mail
- Autenticação via **senha de app Gmail** (segura, sem expor a senha principal)
- Log completo em `dados/email_log.txt`
- Tratamento de erros de autenticação e envio

---

### 📊 Parte 5 — Relatório Excel

- Exporta todas as faturas do banco para planilha `.xlsx`
- Aba **"Faturas"** com cabeçalho colorido e linhas marcadas por status:
  - 🟢 Verde → `enviado`
  - 🟡 Amarelo → `pendente`
  - 🔴 Vermelho → `falhou`
- Aba **"Resumo"** com agrupamento por status, contagem e valor total
- Linha de totais gerais ao final

---

### 🖥️ Opcional — Interface Gráfica (FreeSimpleGUI) `⭐ Bônus`

- Janela com botões coloridos para cada módulo
- Botão **"EXECUTAR TUDO"** roda as partes 2→5 em sequência
- Log em tempo real com output de cada script
- Barra de progresso e indicador de status
- Execução em **thread separada** (não trava a janela durante o processamento)
- Botão para abrir a pasta de boletos diretamente

---

## 🛠️ Tecnologias

| Biblioteca | Uso |
|---|---|
| `Flask` | Framework web para o sistema de cadastro |
| `Selenium` | Automação do navegador Chrome |
| `webdriver-manager` | Gerencia o ChromeDriver automaticamente |
| `openpyxl` | Leitura e escrita de arquivos Excel |
| `ReportLab` | Geração de PDFs |
| `qrcode[pil]` | Geração do QR Code PIX |
| `Pillow` | Manipulação de imagens no PDF |
| `smtplib` | Envio de e-mails via SMTP (built-in) |
| `pyautogui` | Simulação de teclado (WhatsApp) |
| `python-dotenv` | Carregamento de variáveis de ambiente |
| `FreeSimpleGUI` | Interface gráfica desktop |
| `pandas` | Manipulação de dados para o relatório |
| `xlsxwriter` | Engine de escrita Excel com formatação |
| `sqlite3` | Banco de dados relacional (built-in) |

---

## 📦 Pré-requisitos

Antes de começar, verifique se você tem instalado:

- ✅ **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- ✅ **Google Chrome** — versão recente
- ✅ **Conta Gmail** com verificação em duas etapas ativada
- ✅ **Celular com WhatsApp** para escanear o QR Code

---

## ⚙️ Instalação e Configuração

### 1️⃣ Entre na pasta do projeto

```bash
cd av1
```

### 2️⃣ (Recomendado) Crie e ative um ambiente virtual

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux / macOS:
```bash
source venv/bin/activate
```

### 3️⃣ Instale todas as dependências

```bash
pip install flask selenium webdriver-manager openpyxl reportlab "qrcode[pil]" pillow python-dotenv FreeSimpleGUI pandas xlsxwriter pyautogui
```

### 4️⃣ Configure o arquivo `.env`

Edite o arquivo `config/.env` com seus dados:

> **Como gerar a Senha de App do Gmail:**
> 1. Acesse [myaccount.google.com](https://myaccount.google.com)
> 2. Segurança → Verificação em duas etapas → Role até o final
> 3. Clique em **"Senhas de app"**
> 4. Selecione "Outro (nome personalizado)" → gere e copie a senha de 16 caracteres

### 5️⃣ Prepare a planilha de clientes

O arquivo `dados/clientes_importar.xlsx` deve ter as colunas na seguinte ordem:

| A — Nome | B — Email | C — Telefone | D — Endereço |
|---|---|---|---|
| João Silva | joao@email.com | 5548999990001 | Rua A, 123 |
| Maria Souza | maria@email.com | 5548999990002 | Rua B, 456 |

> O telefone deve incluir código do país + DDD, sem espaços ou traços.
> Exemplo: `5548999990001` para número brasileiro de SC.

---

## ▶️ Como Executar

> ⚠️ **IMPORTANTE:** Execute sempre a partir da pasta raiz `av1/`.
> O sistema web deve estar rodando **antes** de qualquer outra etapa.

---

### 🌐 ETAPA 1 — Inicie o Sistema Web

Abra um terminal e deixe rodando:

```bash
python 1parte_web/app.py
```

Acesse em: **http://127.0.0.1:5000**

---

### 🤖 ETAPA 2 — RPA: Importe clientes do Excel

Abra **outro terminal** (mantenha o Flask rodando no anterior):

```bash
python parte1_rpa/rpa_cadastro.py
```

O Chrome abrirá automaticamente e preencherá cada cliente no sistema web.
Ao final, a planilha será atualizada com o status de cada cadastro.

---

### 📄 ETAPA 3 — Gere os Boletos em PDF

```bash
python parte2_pdf/gerar_boletos.py
```

Os PDFs serão salvos em `boletos/` com o nome `boleto_cliente001_NomeCliente.pdf`.

---

### 📱 ETAPA 4 — Envie via WhatsApp Web

```bash
python parte3_whatsapp/enviar_whatsapp.py
```

> Você terá **15 segundos** para escanear o QR Code com seu celular.
> Esse tempo pode ser ajustado em `config/.env` → `ESPERA_WHATSAPP=30`

---

### 📧 ETAPA 5 — Envie os E-mails

```bash
python parte4_email/enviar_email.py
```

Cada cliente receberá um e-mail HTML com o boleto PDF em anexo.

---

### 📊 ETAPA 6 — Gere o Relatório Excel

```bash
python parte5_relatorio/relatorio_excel.py
```

O arquivo será salvo em `dados/faturas_relatorio.xlsx` com duas abas formatadas.

---

## 🖥️ Interface Gráfica (Opcional)

Em vez de rodar cada script manualmente, use a GUI para controlar tudo visualmente:

```bash
python interface/gui.py
```

A janela oferece:
git remote add o_meu https://github.com/mariadelfino/rpa_project.git
| Botão | Ação |
|---|---|
| 🌐 Sistema Web | Inicia o servidor Flask |
| 🤖 RPA Cadastro | Importa clientes do Excel |
| 📄 Gerar Boletos | Gera os PDFs |
| 📱 WhatsApp | Dispara as mensagens |
| 📧 E-mails | Dispara os e-mails com PDF |
| 📊 Relatório | Gera o Excel |
| 🚀 EXECUTAR TUDO | Roda as partes 2 a 5 em sequência |
| 📂 Pasta Boletos | Abre a pasta de boletos no explorador |

---

## 🗄️ Banco de Dados

O banco SQLite (`1parte_web/techsolutions.db`) possui duas tabelas com relacionamento:

```sql
-- Tabela de clientes
CREATE TABLE clientes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT    NOT NULL,
    email         TEXT    NOT NULL,
    telefone      TEXT    NOT NULL,
    endereco      TEXT,
    data_cadastro TEXT    DEFAULT (date('now'))
);

-- Tabela de faturas (relacionada com clientes via FK)
CREATE TABLE faturas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id      INTEGER NOT NULL,
    valor           REAL    NOT NULL,
    data_vencimento TEXT    NOT NULL,
    status          TEXT    DEFAULT 'pendente',
    data_emissao    TEXT    DEFAULT (date('now')),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
```

**Ciclo de vida do status de uma fatura:**

```
pendente  ──►  enviado
    │
    └────────►  falhou
```

---

## 📸 Exemplos de Saída

### Boleto PDF Gerado

```
┌─────────────────────────────────────────┐
│          TechSolutions Ltda             │
│           BOLETO DE COBRANÇA            │  Fatura Nº 00001
├─────────────────────────────────────────┤
│ DADOS DO CLIENTE                        │
│ Nome:     Carlos Eduardo Lima           │
│ E-mail:   carlos@email.com              │
│ Telefone: 5548999990001                 │
├─────────────────────────────────────────┤
│ DADOS DO BOLETO                         │
│ Valor:    R$ 1.500,00                   │
│ Vencimento:      31/03/2026             │
│ Data de Emissão: 27/03/2026             │
│ [ 0001.0001 150000.0 12345.678901 ... ] │
│                                         │
│              [ QR CODE ]                │
│    📱 Pague via PIX — Escaneie          │
│      Leia com o app do seu banco        │
└─────────────────────────────────────────┘
```

### Mensagem WhatsApp

```
Olá, *Carlos Eduardo Lima*! 👋

Notificação automática da *TechSolutions Ltda*.

📄 *Fatura #00001*
💰 Valor: *R$ 1.500,00*
📅 Vencimento: *31/03/2026*

Pague pelo QR Code PIX:
🔗 http://127.0.0.1:5000/boletos/boleto_cliente001_Carlos_Eduardo_Lima.pdf

Dúvidas? Responda esta mensagem.
_TechSolutions Ltda — Financeiro_ 🏢
```

### Output do Terminal (RPA)

```
==================================================
  🤖 RPA - Cadastro Automático de Clientes
==================================================

📊 Lendo: dados/clientes_importar.xlsx
✅ 5 clientes encontrados

🌐 Iniciando Chrome...

[1/5] Cadastrando: Carlos Eduardo Lima...
   ✅ Sucesso!
[2/5] Cadastrando: Ana Paula Souza...
   ✅ Sucesso!
[3/5] Cadastrando: Marcos Henrique...
   ✅ Sucesso!
[4/5] Cadastrando: Fernanda Costa...
   ✅ Sucesso!
[5/5] Cadastrando: Rafael Oliveira...
   ✅ Sucesso!

📊 Planilha atualizada: dados/clientes_importar.xlsx
📊 RESUMO: 5/5 cadastrados!
```

---

## ⚠️ Observações Importantes

| Ponto | Descrição |
|---|---|
| 🔑 **Credenciais** | Nunca suba o `config/.env` para repositórios públicos. Adicione ao `.gitignore`. |
| 🌐 **Ordem de execução** | O servidor Flask **deve estar rodando** antes de qualquer outra etapa. |
| 📱 **WhatsApp** | Exige celular físico com WhatsApp para escanear o QR Code a cada nova sessão do Chrome. |
| 📄 **Boletos antes do e-mail** | Os PDFs precisam existir em `/boletos` antes de disparar os e-mails. |
| 📁 **Diretório raiz** | Execute todos os scripts **a partir da pasta raiz** `av1/` para os caminhos relativos funcionarem. |
| 🔐 **Senha de App Gmail** | Use **senha de app** de 16 caracteres, não a senha da conta Google. Requer 2FA ativado. |
| 🔁 **Sessão WhatsApp** | Para manter a sessão entre execuções, descomente a linha `--user-data-dir` em `enviar_whatsapp.py`. |

---

## 📁 Arquivo `.gitignore` Recomendado

```gitignore
# Credenciais — NUNCA commitar
config/.env

# Banco de dados
*.db

# Boletos gerados
boletos/

# Cache Python
__pycache__/
*.pyc
*.pyo

# Ambiente virtual
venv/
.venv/

# Logs e relatórios gerados
dados/email_log.txt
dados/erros.csv
dados/faturas_relatorio.xlsx
```

---

<div align="center">

---

Feito com 🐍 Python · Disciplina **Linguagem de Programação III** · 2026

</div>