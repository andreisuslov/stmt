NAME := stmt

# Define variables based on the operating system
ifeq ($(OS),Windows_NT)
    PYTHON := python
    PIP := pip
else
    PYTHON := $(shell poetry env info -p)/bin/python
    PIP := $(shell poetry env info -p)/bin/pip
endif

.PHONY: install reinstall clean help

install:
	@echo "Checking if pipx is installed..."
	@$(PIP) show pipx &> /dev/null || $(PIP) install pipx
	@pipx ensurepath
	@echo "Configuring the project using Poetry..."
	@poetry lock || exit 1
	@poetry install --no-root || exit 1
	@echo "Installing $(NAME) using Python from Poetry's virtual environment..."
	@if pipx list | grep -q $(NAME); then \
		echo "$(NAME) is already installed. Skipping installation."; \
	else \
		pipx install . --python $(PYTHON); \
	fi

reinstall:
	@echo "Reinstalling $(NAME)..."
	@pipx uninstall "$(NAME)" || true
	@pipx install . --python $(PYTHON)
	@echo "$(NAME) has been reinstalled."

clean:
	@echo "Cleaning up..."
	@rm -rf $(shell poetry env info -p) || exit 1

help:
	@echo "Makefile commands:"
	@echo "install - Install the application and all dependencies"
	@echo "reinstall - Reinstall the application"
	@echo "clean - Remove Python file artifacts and virtual environment"
	@echo "help - Display this help message"

.DEFAULT_GOAL := help
