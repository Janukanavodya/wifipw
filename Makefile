.PHONY: test install clean coverage lint help

# Default target
help:
	@echo "Available targets:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run all tests"
	@echo "  coverage   - Run tests with coverage report"
	@echo "  lint       - Run code linting (if flake8 is available)"
	@echo "  clean      - Clean up generated files"
	@echo "  help       - Show this help message"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python -m pytest

# Run tests with coverage
coverage:
	python -m pytest --cov=wifipw --cov-report=term-missing --cov-report=html

# Run linting if flake8 is available
lint:
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 wifipw.py test_wifipw.py; \
	else \
		echo "flake8 not available, skipping lint"; \
	fi

# Clean generated files
clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete