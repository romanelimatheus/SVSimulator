bin := .venv/bin

install-dev:
	python3 -m venv .venv
	$(bin)/python -m pip install uv
	$(bin)/uv pip install -e .[dev]

install-deps:
	sudo apt-get update && sudo apt-get install libegl1 -y

pytest:
	$(bin)/pytest .

ruff:
	$(bin)/ruff check .

ruff-fix:
	$(bin)/ruff check --fix .

mypy:
	$(bin)/mypy .

qa: pytest ruff mypy

run:
	$(bin)/python -m src.__main__
