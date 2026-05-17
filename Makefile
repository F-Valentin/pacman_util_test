NAME = pac_man
PYTHON = python3
VENV = venv
BIN = $(VENV)/bin
MAIN = src/pac-man.py
CONFIG_FILE ?= config/config.json

.PHONY: install run debug clean lint
.SILENT:

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r config/requirements.txt

run:
	$(BIN)/python $(MAIN) $(CONFIG_FILE)

debug:
	$(BIN)/python -m pdb $(MAIN) $(CONFIG_FILE)

clean:
	rm -rf $(VENV)
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

lint:
	$(BIN)/flake8 . --exclude=$(VENV)
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores \
	    --ignore-missing-imports --disallow-untyped-defs \
	    --check-untyped-defs --exclude $(VENV)

.PHONY: all run clean