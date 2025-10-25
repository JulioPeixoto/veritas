# Veritas

API FastAPI para processamento de dados.

## Pré-requisitos
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (gerenciador de dependências)
- [.env](#arquivo-env) com variáveis de API (OpenAI e SerpAPI)

## Instalação de dependências (usando uv)
```bash
uv pip install -r requirements.txt
```
Ou via Makefile:
```bash
make uv
```

## Como iniciar com uv
```bash
uvicorn src.main:app --reload
```

## Arquivo .env
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```
OPENAI_API_KEY=seu_token_openai
erp_API_KEY=seu_token_serpapi
```

Ajuste os nomes acima conforme necessários pelo seu app (consulte `src/config.py`). Estes tokens são obrigatórios para a operação dos módulos de processamento de linguagem e scraping.

## Comandos

### Iniciar servidor de desenvolvimento
```bash
make dev
```

### Instalar dependências com uv
```bash
make uv
```

## Referências externas importantes
- [Documentação OpenAI API](https://platform.openai.com/docs)
- [Documentação SerpAPI](https://serpapi.com/docs)
