ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

build: test_requirements test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

flake8:
	flake8 . \
	--exclude=.venv,venv,node_modules,migrations \
	--max-line-length=120

pytest:
	pytest . --capture=no --cov=. --cov-config=.coveragerc -vv $(ARGUMENTS)

test_requirements:
	pip install -e .[test]

CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test: flake8 pytest
	$(CODECOV)

publish:
	rm -rf build dist; \
	python setup.py bdist_wheel; \
	twine upload --username $$DIRECTORY_PYPI_USERNAME --password $$DIRECTORY_PYPI_PASSWORD dist/*

.PHONY: build clean test_requirements flake8 pytest test publish
