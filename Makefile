.PHONY: tests docs

deps: 
	@echo "Initializing Git..."
	git init
	
	@echo "Installing dependencies..."
	pip install -r requirements-dev.txt
	pre-commit install
	
tests:
	pytest

docs:
	@echo Save documentation to docs... 
	pdoc src -o docs --force
	@echo View API documentation... 
	pdoc src --http localhost:8080	
