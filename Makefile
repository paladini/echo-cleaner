.PHONY: help install install-dev run clean build-appimage test format lint

help:
	@echo "Echo Clear - Makefile Commands"
	@echo ""
	@echo "  make install        - Install dependencies"
	@echo "  make install-dev    - Install dev dependencies"
	@echo "  make run           - Run the application"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make build-appimage - Build AppImage for distribution"
	@echo "  make test          - Run tests"
	@echo "  make format        - Format code with black"
	@echo "  make lint          - Lint code with flake8"

install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev]"

run:
	python3 echo-clear.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf app/__pycache__
	rm -rf app/*/__pycache__
	rm -f EchoCleaner-*.AppImage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build-appimage:
	@echo "Building AppImage..."
	@chmod +x scripts/build_appimage.sh
	@./scripts/build_appimage.sh

test:
	pytest tests/ -v

format:
	black app/ echo-clear.py

lint:
	flake8 app/ echo-clear.py
