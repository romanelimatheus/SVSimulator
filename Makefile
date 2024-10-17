bin := .venv/bin

install-dev:
	python3 -m venv .venv
	$(bin)/python -m pip install uv
	$(bin)/uv pip install -e .[dev]

pytest:
	$(bin)/pytest .

ruff:
	$(bin)/ruff check .

ruff-fix:
	$(bin)/ruff check --fix .

mypy:
	$(bin)/mypy .

qa: pytest ruff mypy
