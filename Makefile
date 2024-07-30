.PHONY: all install uninstall clean

VENV_NAME = .venv
PY = ./$(VENV_NAME)/bin/python

PACKAGES = $(PY) -m pip freeze | sed -E "s/==[^$$]+/ /" | tr -d '\n'

all: venv upgrade install

venv:
	python3 -m venv $(VENV_NAME)

upgrade:
	$(PY) -m pip install --upgrade pip

install:
	$(PY) -m pip install -r requirements.txt

uninstall:
	$(PY) -m pip uninstall $(PACKAGES)

clean:
	rm -rf venv __pycache__

freeze:
	$(PY) -m pip freeze

req-update:
	$(PY) -m pip freeze > requirements.txt
