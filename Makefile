dev:
	uv run fastapi dev src/main.py --reload --port 8001

install uv:
	pip install -U pip && pip install uv

format:
	black .
	isort .

lint:
	flake8 .

check:
	uv run black --check --diff .
	uv run isort --profile black --check-only --diff .
	uv run flake8 .