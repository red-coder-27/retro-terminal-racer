# Terminal Racer Makefile

.PHONY: run test clean install help

# Default target
help:
	@echo "Terminal Racer Development Commands:"
	@echo "  make run      - Run the game"
	@echo "  make test     - Test code structure"
	@echo "  make clean    - Clean generated files"
	@echo "  make install  - Make game executable"
	@echo "  make package  - Create distribution package"
	@echo "  make help     - Show this help"

# Run the game
run:
	@echo "🏁 Starting Terminal Racer..."
	python3 terminal_racer.py

# Test the code structure
test:
	@echo "🧪 Testing game structure..."
	python3 test_game.py

# Clean generated files
clean:
	@echo "🧹 Cleaning up..."
	rm -f high_score.json
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Make the game executable
install:
	@echo "📦 Making game executable..."
	chmod +x terminal_racer.py
	@echo "✅ You can now run: ./terminal_racer.py"

# Create a simple distribution
package: clean
	@echo "📦 Creating package..."
	mkdir -p dist
	cp terminal_racer.py dist/
	cp README.md dist/
	cp ENHANCEMENTS.md dist/
	cp DEVELOPMENT.md dist/
	cd dist && tar -czf terminal-racer.tar.gz *
	@echo "✅ Package created: dist/terminal-racer.tar.gz"

# Development mode - run with debug info
debug:
	@echo "🐛 Running in debug mode..."
	python3 -u terminal_racer.py

# Check Python version and dependencies
check:
	@echo "🔍 Checking system requirements..."
	@python3 --version
	@python3 -c "import curses; print('✅ curses module available')"
	@python3 -c "import json; print('✅ json module available')"
	@python3 -c "import random; print('✅ random module available')"
	@python3 -c "import time; print('✅ time module available')"
	@echo "✅ All dependencies satisfied"

# Show game statistics
stats:
	@echo "📊 Game Statistics:"
	@wc -l terminal_racer.py | awk '{print "Lines of code: " $$1}'
	@grep -c "def " terminal_racer.py | awk '{print "Functions: " $$1}'
	@grep -c "class " terminal_racer.py | awk '{print "Classes: " $$1}'
	@if [ -f high_score.json ]; then \
		echo "High Score: $$(cat high_score.json | grep -o '[0-9]*')"; \
	else \
		echo "High Score: Not set"; \
	fi
