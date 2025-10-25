# Veritas

FastAPI-based data processing API.

## Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (dependency manager)
- [.env](#env-file) file with required API variables (OpenAI and SerpAPI)

## Installing dependencies (using uv)
```bash
uv pip install -r requirements.txt
```
Or via Makefile:
```bash
make uv
```

## How to start using uv
```bash
uvicorn src.main:app --reload
```

## .env file
Create a `.env` file at the root of the project with the following content:
```
OPENAI_API_KEY=your_openai_token
SERP_API_KEY=your_serpapi_token
```

Adjust the names above as needed (check `src/config.py`). These tokens are required for language and scraping modules to work.

## Commands

### Start development server
```bash
make dev
```

### Install dependencies with uv
```bash
make uv
```

## Important External References
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [SerpAPI Documentation](https://serpapi.com/docs)
