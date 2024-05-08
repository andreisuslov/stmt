NAME := stmt

.PHONY: install reinstall clean

install:
	@echo "Installing pipx if not already installed..."
	@brew list pipx || brew install pipx || exit 1
	@pipx ensurepath
	@echo "Configuring the project using Poetry..."
	@poetry lock || exit 1
	@poetry install --no-root || exit 1
	@echo "Installing $(NAME) using Python from Poetry's virtual environment..."
	@if pipx list | grep -q $(NAME); then \
		echo "$(NAME) is already installed. Skipping installation."; \
	else \
		pipx install .; \
	fi

reinstall:
	@echo "Reinstalling $(NAME)..."
	@pipx uninstall "$(NAME)" || true
	@pipx install . --python $$(poetry env info -p)/bin/python
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
