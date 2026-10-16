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

deb:
	@mkdir -p dist /tmp/epicmarker_deb/DEBIAN /tmp/epicmarker_deb/usr/bin /tmp/epicmarker_deb/usr/lib/python3/dist-packages/epicmarker /tmp/epicmarker_deb/usr/share/applications /tmp/epicmarker_deb/usr/share/icons/hicolor/256x256/apps
	@cp -r epicmarker/* /tmp/epicmarker_deb/usr/lib/python3/dist-packages/epicmarker/
	@cp assets/epicmarker.png /tmp/epicmarker_deb/usr/share/icons/hicolor/256x256/apps/epicmarker.png
	@printf '#!/usr/bin/env bash\nif [ -n "$$WAYLAND_DISPLAY" ] && [ -z "$$GDK_BACKEND" ]; then\n    export GDK_BACKEND=x11\nfi\nexec python3 -m epicmarker.main "$$@"\n' > /tmp/epicmarker_deb/usr/bin/epicmarker
	@chmod 755 /tmp/epicmarker_deb/usr/bin/epicmarker
	@printf '[Desktop Entry]\nName=EpicMarker\nComment=Desktop marker and screen annotation tool like Epic Pen\nExec=/usr/bin/epicmarker\nIcon=epicmarker\nTerminal=false\nType=Application\nCategories=Utility;Graphics;\nKeywords=screen;marker;draw;pen;epic;annotation;presentation;whiteboard;\nStartupNotify=true\n' > /tmp/epicmarker_deb/usr/share/applications/epicmarker.desktop
	@printf 'Package: epicmarker\nVersion: 1.0.0\nSection: utils\nPriority: optional\nArchitecture: all\nDepends: python3, python3-gi, python3-gi-cairo, gir1.2-gtk-3.0, libcairo2\nMaintainer: Khitish Nayak <kknayak049@gmail.com>\nHomepage: https://github.com/Khitishnayak/epicmarker\nDescription: Desktop marker and screen annotation tool like Epic Pen\n' > /tmp/epicmarker_deb/DEBIAN/control
	@dpkg-deb --build --root-owner-group /tmp/epicmarker_deb dist/epicmarker_1.0.0_all.deb
	@rm -rf /tmp/epicmarker_deb
	@echo "✓ Built dist/epicmarker_1.0.0_all.deb"

lint:
	python3 -m flake8 epicmarker tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info
