# Desafio Técnico – Desenvolvedor Python Conthabil (Automação com Selenium)

## Funcionalidades

- **Bot (Selenium)**
Automação em Python que:
  - Acessa o site da prefeitura de Natal e baixa todas as publicações referentes ao mês anterior.
  - Baixa o documento de cada publicação e armazena localmente em `/pdfs`.
  - Realiza o upload dos arquivos no serviço de armazenamento online: **https://0x0.st**.  
  - Armazena as URL´s de cada arquivo e dá um print no terminal.
  - Insere a URL de cada arquivo em um banco de dados PostgreSQL, acompanhada da data de publicação dos arquivos, através da API desenvolvida. 

- **API (Django)**
  - **Lista** todos os diários cadastrados.
  - **Filtra** os diários por mês.

--- 

## Requisitos

- [Python 3.9+](https://www.python.org/)
- [Docker](https://docs.docker.com/get-docker/)
- Dependências: veja `requirements.txt`

---

## Estrutura do Projeto 

```
api_diarios/                 # Aplicação Django (API)
├── api_diarios/             # Configurações e app principal do Django
├── arquivos/                # (opcional) arquivos de suporte
├── docker-compose.yml       # Orquestra containers (API + DB)
├── Dockerfile               # Build da API
├── manage.py                # Comando principal do Django
└── requirements.txt         # Dependências da API

bot/                         # Bot de coleta dos diários (Selenium)
├── pdfs/                    # PDFs baixados
├── config.json              # Configurações do bot
├── prefeituraNatal.py       # Script de scraping
└── requirements.txt         # Dependências do bot

venv/                        # Ambiente virtual (não versionar)
```
---

###  Clonar o repositório
```bash
git clone https://github.com/lauralima6/api_diarios.git
cd api_diarios
```

###  Subir com Docker
```bash
docker-compose up --build

```
A API ficará disponível em:
```
http://31.97.161.248:8000/apipublicacoes/
```

---
## Rotas da API

- **Listar todos os diários**
  ```
  GET /apipublicacoes/diarios/
  ```

- **Filtrar por mês**
  ```
  GET /apipublicacoes/?mes=08
  ```
---

## Executar o Bot

### Instalar dependências
```bash
cd bot
pip install -r requirements.txt
```

### Rodar o bot
```bash
python prefeituraNatal.py
```

Após rodar:
- PDFs estarão em `bot/pdfs/`
- URLs e datas estarão registradas no banco

---

## Tecnologias Usadas
- **Django + Django REST Framework** → API
- **PostgreSQL** → Banco de dados
- **Selenium** → Automação e scraping
- **Docker + Docker Compose** → Containerização

---