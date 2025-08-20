dev:
	uv run fastapi dev src/main.py --reload --port 8001

install uv:
	pip install -U pip && pip install uv