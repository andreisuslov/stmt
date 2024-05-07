.PHONY: install

install:
	@echo "Installing pipx if not already installed..."
	@brew list pipx || brew install pipx
	@pipx ensurepath
	@echo "Configuring the project using Poetry..."
	@poetry lock
	@poetry install --no-root
	@echo "Installing the CLI tool globally using pipx..."
	@pipx install .

clean:
	@echo "Cleaning up..."
	@rm -rf $(shell poetry env info -p)

help:
	@echo "Makefile commands:"
	@echo "install - Install the application and all dependencies"
	@echo "clean - Remove Python file artifacts and virtual environment"
	@echo "help - Display this help message"

.DEFAULT_GOAL := help
