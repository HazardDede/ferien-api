.PHONY: clean-pyc clean-build clean lint test doctest rollback version

VERSION='0.3.7'
SOURCE_PATH=./ferien
TEST_PATH=./tests

# Environment overrides
VERSION_PART?=patch

help:
		@echo "    clean"
		@echo "        Remove python and release artifacts."
		@echo "    setup"
		@echo "        Installs dependencies into the environment"
		@echo "    lint"
		@echo "        Check style with flake8."
		@echo "    test"
		@echo "        Run py.test"
		@echo "    doctest"
		@echo "        Run doctest"
		@echo "    version"
		@echo "        Prints out the current version"
		@echo "    release-test"
		@echo "        Bundles a release and deploys it to test.pypi"
		@echo "    release"
		@echo "        Bundles a release and deploys it to pypi"

clean-pyc:
		find . -name '*.pyc' -delete
		find . -name '*.pyo' -delete
		# find . -name '*~' -exec rm --force  {} +

clean-build:
		rm -rf build/
		rm -rf dist/
		rm -rf *.egg-info
		rm -rf .pytest_cache

clean: clean-pyc clean-build

setup:
		pip install pip --upgrade
		pip install -r requirements.txt --upgrade

docs: README.mdpp
		markdown-pp README.mdpp -o README.md

lint:
		flake8 $(SOURCE_PATH)
		pylint $(SOURCE_PATH)
		mypy --strict --no-warn-unused-ignores $(SOURCE_PATH)

test:
		pytest --verbose --color=yes -s \
			--doctest-modules \
			--cov=$(SOURCE_PATH) --cov-report html --cov-report term $(TEST_PATH) \
			$(SOURCE_PATH)

doctest:
		pytest --verbose --color=yes --doctest-modules $(SOURCE_PATH)

version:
		@echo $(VERSION)

next-version: lint test
		$(eval NEXT_VERSION := $(shell bumpversion --dry-run --allow-dirty --list $(VERSION_PART) | grep new_version | sed s,"^.*=",,))
		@echo Next version is $(NEXT_VERSION)
		bumpversion $(VERSION_PART)
		@echo "Review your version changes first"
		@echo "Accept your version: \`make accept-version\`"
		@echo "Revoke your version: \`make revoke-version\`"

accept-version:
		git push && git push --tags

revoke-version:
		git tag -d `git describe --tags --abbrev=0`    # delete the tag
		git reset --hard HEAD~1                        # rollback the commit

sdist:
		rm -f dist/*
		python setup.py sdist

release-test: sdist
		twine upload dist/* -r testpypi

release: sdist
		twine upload dist/* -r pypi
