bin := .venv/bin

install-dev:
	python3 -m venv .venv
	$(bin)/python -m pip install uv
	$(bin)/uv pip install -e .[dev]

sudo-install:
	sudo $(bin)/python -m pip install uv
	sudo $(bin)/uv pip install -e .[dev]

install-deps:
	sudo apt-get update && sudo apt-get install -y --no-install-recommends libegl1
	sudo apt install libxcb-cursor0

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
	sudo $(bin)/python -m src.__main__
