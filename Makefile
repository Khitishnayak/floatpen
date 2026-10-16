.PHONY: run test install uninstall deb lint clean

run:
	./run.sh

test:
	python3 -m unittest discover -s tests -v

install:
	./install.sh

uninstall:
	rm -f $(HOME)/.local/bin/floatpen
	rm -f $(HOME)/.local/share/applications/floatpen.desktop
	rm -f $(HOME)/.local/share/icons/hicolor/256x256/apps/floatpen.png
	@echo "✓ FloatPen uninstalled."

deb:
	@mkdir -p dist /tmp/floatpen_deb/DEBIAN /tmp/floatpen_deb/usr/bin /tmp/floatpen_deb/usr/lib/python3/dist-packages/floatpen /tmp/floatpen_deb/usr/share/applications /tmp/floatpen_deb/usr/share/icons/hicolor/256x256/apps
	@cp -r floatpen/* /tmp/floatpen_deb/usr/lib/python3/dist-packages/floatpen/
	@cp assets/floatpen.png /tmp/floatpen_deb/usr/share/icons/hicolor/256x256/apps/floatpen.png
	@printf '#!/usr/bin/env bash\nif [ -n "$$WAYLAND_DISPLAY" ] && [ -z "$$GDK_BACKEND" ]; then\n    export GDK_BACKEND=x11\nfi\nexec python3 -m floatpen.main "$$@"\n' > /tmp/floatpen_deb/usr/bin/floatpen
	@chmod 755 /tmp/floatpen_deb/usr/bin/floatpen
	@printf '[Desktop Entry]\nName=FloatPen\nComment=Floating desktop marker and screen annotation tool like Epic Pen\nExec=/usr/bin/floatpen\nIcon=floatpen\nTerminal=false\nType=Application\nCategories=Utility;Graphics;\nKeywords=screen;marker;draw;pen;epic;annotation;presentation;whiteboard;floating;\nStartupNotify=true\n' > /tmp/floatpen_deb/usr/share/applications/floatpen.desktop
	@printf 'Package: floatpen\nVersion: 1.0.0\nSection: utils\nPriority: optional\nArchitecture: all\nDepends: python3, python3-gi, python3-gi-cairo, gir1.2-gtk-3.0, libcairo2\nMaintainer: Khitish Nayak <kknayak049@gmail.com>\nHomepage: https://github.com/Khitishnayak/floatpen\nDescription: Floating desktop marker and screen annotation tool like Epic Pen\n' > /tmp/floatpen_deb/DEBIAN/control
	@dpkg-deb --build --root-owner-group /tmp/floatpen_deb dist/floatpen_1.0.0_all.deb
	@rm -rf /tmp/floatpen_deb
	@echo "✓ Built dist/floatpen_1.0.0_all.deb"

lint:
	python3 -m flake8 floatpen tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info
