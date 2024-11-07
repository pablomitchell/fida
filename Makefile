.PHONY: deps install install-dev install-test update clean lint format check test

# Generate all dependency files from pyproject.toml
deps:
	python scripts/generate_dependencies.py

# Install different dependency sets
install:
	uv pip install -r requirements.txt

install-test: install
	uv pip install -r requirements-test.txt

install-dev: install-test
	uv pip install -r requirements-dev.txt

# Update dependencies to latest versions
update:
	uv pip compile --upgrade requirements.in -o requirements.txt
	uv pip compile --upgrade requirements-test.in -o requirements-test.txt
	uv pip compile --upgrade requirements-dev.in -o requirements-dev.txt
	uv pip install -r requirements-dev.txt

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .ruff_cache/ .mypy_cache/

# Code quality commands
format:
	ruff format .
	ruff check . --fix

lint:
	ruff check .
	mypy .

check: format lint

test:
	pytest