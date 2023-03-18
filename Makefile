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
	@./venv/bin/python -m nuitka --standalone  --follow-imports --onefile main.py

publish:
	./venv/bin/pip install twine
	rm -rf build dist q.egg-info
	find -name *.pyc -delete
	./venv/bin/python setup.py sdist
	./venv/bin/python python setup.py bdist_wheel
	./venv/bin/twine upload dist/*

