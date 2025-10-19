.PHONY: help install install-dev run clean build-appimage download-tools test format lint

help:
	@echo "Echo Clear - Makefile Commands"
	@echo ""
	@echo "  make install        - Install dependencies"
	@echo "  make install-dev    - Install dev dependencies"
	@echo "  make run           - Run the application"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make download-tools - Download build tools (appimagetool)"
	@echo "  make build-appimage - Build AppImage for distribution"
	@echo "  make test          - Run tests"
	@echo "  make format        - Format code with black"
	@echo "  make lint          - Lint code with flake8"

install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev]"

run:
	python3 echo-cleaner.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf app/__pycache__
	rm -rf app/*/__pycache__
	rm -f EchoCleaner-*.AppImage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-all: clean
	rm -rf tools/

build-appimage:
	@echo "Building AppImage..."
	@chmod +x scripts/build_appimage.sh
	@./scripts/build_appimage.sh

download-tools:
	@echo "Downloading build tools..."
	@mkdir -p tools
	@if [ ! -f "tools/appimagetool-x86_64.AppImage" ]; then \
		echo "Downloading appimagetool..."; \
		wget -q --show-progress -O tools/appimagetool-x86_64.AppImage \
			https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage; \
		chmod +x tools/appimagetool-x86_64.AppImage; \
		echo "✓ appimagetool downloaded successfully"; \
	else \
		echo "✓ appimagetool already exists"; \
	fi

test:
	pytest tests/ -v

format:
	black app/ echo-cleaner.py

lint:
	flake8 app/ echo-cleaner.py
