# Makefile for blackjack.py

# Variables
PYTHON = python3
SRC_FILE = blackjack.py

# Targets
.PHONY: all run clean

all: run

run:
	@$(PYTHON) $(SRC_FILE)

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
