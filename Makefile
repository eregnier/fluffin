.PHONY: all test clean build dist

install:
	rm -rf venv
	python3 -m virtualenv venv
	./venv/bin/pip install -r requirements.txt

dev:
	@./venv/bin/python main.py --dev

build:
	@./venv/bin/python main.py

build-dist:
	@./venv/bin/python -m pip install nuitka
	@python -m nuitka --standalone  --follow-imports --onefile main.py
