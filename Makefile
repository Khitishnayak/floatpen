.PHONY: run test install uninstall lint clean

run:
	./run.sh

test:
	python3 -m unittest discover -s tests -v

install:
	./install.sh

uninstall:
	rm -f $(HOME)/.local/bin/epicmarker
	rm -f $(HOME)/.local/share/applications/epicmarker.desktop
	rm -f $(HOME)/.local/share/icons/hicolor/256x256/apps/epicmarker.png
	@echo "✓ EpicMarker uninstalled."

lint:
	python3 -m flake8 epicmarker tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info
