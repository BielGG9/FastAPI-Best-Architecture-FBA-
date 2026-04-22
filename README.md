# FastAPI MPE Fiscalização

Um sistema de gerenciamento (CRUD completo) para **Estados** e **Municípios**, desenvolvido utilizando o ecossistema moderno do Python com foco em alta performance e manutenibilidade. 

Este projeto adere fortemente aos padrões da **FastAPI Best Architecture (FBA)**, separando as responsabilidades em camadas distintas para garantir um código limpo, testável e escalável.

---

## 🚀 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno e rápido para a construção de APIs.
- **[SQLModel](https://sqlmodel.tiangolo.com/):** Ferramenta para iteração com banco de dados em Python, unindo SQLAlchemy e Pydantic.
- **[PostgreSQL](https://www.postgresql.org/):** Sistema de banco de dados relacional (via Docker).
- **[Asyncpg](https://magicstack.github.io/asyncpg/):** Driver assíncrono para o banco de dados PostgreSQL.
- **[Pydantic v2](https://docs.pydantic.dev/latest/):** Validação de dados robusta e parseamento usando *type hints* do Python.
- **[Docker & Docker Compose](https://www.docker.com/):** Orquestração e containerização dos serviços.

---

## 🏗️ Arquitetura do Projeto (FastAPI Best Architecture)

O projeto está dividido em camadas com responsabilidades bem definidas (Domain-Driven Design / N-Tier Architecture):

```text
app/
├── api/             # Camada de Apresentação (Routers / Endpoints)
│   └── v1/
│       ├── api.py           # Agregador de todas as rotas da v1
│       └── endpoints/       # Controladores que mapeiam as requisições HTTP (estado.py, municipio.py)
├── core/            # Configurações Essenciais
│   ├── config.py            # Variáveis de ambiente e secrets (BaseSettings)
│   └── database.py          # Configuração da engine e sessão assíncrona do DB
├── crud/            # Camada de Acesso a Dados (Repositories)
│   ├── crud_estado.py       # Queries específicas de banco para 'Estado'
│   └── crud_municipio.py    # Queries específicas de banco para 'Municipio'
├── models/          # Camada de Entidades de Banco (SQLModel table=True)
│   ├── estado.py            # Esquema da tabela 'estado'
│   └── municipio.py         # Esquema da tabela 'municipio'
├── schemas/         # Camada de Transferência de Dados (DTOs via Pydantic)
│   ├── estado.py            # Validações de request/response (Create, Read, Update)
│   └── municipio.py         # Validações de request/response para Município
├── services/        # Camada de Regras de Negócio (Use Cases)
│   ├── estado_service.py    # Lógica de validação (ex: Siglas únicas) antes do CRUD
│   └── municipio_service.py # Lógica de validação (ex: Validar existência do estado_id)
└── main.py          # Ponto de entrada da aplicação e setup (Lifespan)
```

### O Fluxo de Dados

`Requisição HTTP` ➔ `app/api/ (Endpoint)` ➔ `app/services/ (Regra de Negócio)` ➔ `app/crud/ (Banco de Dados)` ➔ `PostgreSQL`

Ao adotar essa separação, o **Router** (api) não sabe como os dados são salvos, e o **CRUD** não sabe sobre as regras de negócio. Isso permite que qualquer camada seja refatorada e testada de forma isolada.

---

## 🛠️ Como Executar o Projeto

O projeto é inteiramente gerenciado por Docker, portanto não há necessidade de configurar um ambiente virtual Python local se não desejar.

**1. Clone ou entre no repositório do projeto:**
```bash
cd FastAPI
```

**2. Suba a infraestrutura usando o Docker Compose:**
```bash
docker compose up -d --build
```
Este comando construirá a imagem da API e iniciará os containers:
- `mpe_db`: Banco de Dados PostgreSQL (porta 5433 host / 5432 container).
- `fba_server`: Servidor FastAPI com Uvicorn (porta 8000).

O Uvicorn iniciará com a flag `--reload` (modo watch). Qualquer alteração que você fizer no código na pasta local refletirá instantaneamente dentro do container.

**3. Teste o acesso:**
O servidor estará disponível em: [http://localhost:8000](http://localhost:8000)

---

## 📚 Documentação da API (Swagger UI)

A FastAPI gera automaticamente uma documentação OpenAPI/Swagger. Com o servidor rodando, você pode acessá-la via navegador:

🔗 **[Documentação Interativa (Swagger): http://localhost:8000/docs](http://localhost:8000/docs)**

Na interface visual, você pode testar todas as rotas (POST, GET, PUT, DELETE) criadas para os CRUDs de Estado e Município, como por exemplo:
- Cadastrar um Estado passando nome e sigla.
- Cadastrar um Município vinculando ao id de um Estado existente.
- Recuperar listas populadas automaticamente.

---

## 🛑 Parando a Execução

Para parar os serviços do docker sem apagar os dados:
```bash
docker compose stop
```

Para remover os containers completamente (os volumes de banco de dados permanecerão persitidos em `postgres_data`):
```bash
docker compose down
```
