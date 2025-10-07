dev:
	uv run fastapi dev src/main.py --reload --port 8001

uv:
	pip install -U pip && pip install uv

# Formatação de código
format:
	black .
	isort .

# Linting de código
lint:
	flake8 .

check:
	uv run black --check --diff .
	uv run isort --profile black --check-only --diff .
	uv run flake8 .