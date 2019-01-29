ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

setup:

	conda env update -f conda.yml --prune

.PHONY: clean
clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {}

.PHONY: autopep8
autopep8:
	DE_ENV=test PYTHONPATH=$(ROOT_DIR) autopep8 --aggressive -r --in-place ebrandz test

.PHONY: isort
isort:
	sh -c "isort --skip-glob=.tox --recursive ebrandz test"

.PHONY: lint
lint:
	DE_ENV=test PYTHONPATH=$(ROOT_DIR) flake8 --exclude=.tox ebrandz test

fix: isort autopep8