.PHONY: all install uninstall clean

VENV_NAME = .venv
PY = ./$(VENV_NAME)/bin/python

all: req venv upgrade install

req:
	sudo apt install python3.12 python3-pip python3-venv redis -y

venv:
	python3 -m venv $(VENV_NAME)

upgrade:
	$(PY) -m pip install --upgrade pip

install:
	$(PY) -m pip install -r requirements.txt
