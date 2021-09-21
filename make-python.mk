# Python standard targets

.PHONY: lint-make
lint-make:
	pylint --generate-rcfile > .pylintrc
	echo "[pydocstyle]\nignore=" > .pydocstylerc

.PHONY: lint-all
lint-all: lint lint-sec lint-type lint-docstring

.PHONY: lint
lint:
	@printf -- "\n\033[33;1m>>> Linting... \033[0m\n"
	@for PY_FOLDER in $(PY_FOLDERS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		printf -- "\033[34;1mpylint \033[0m \n"; \
		pylint $$PY_FOLDER || echo "failed, continue..."; \
		printf -- "\033[34;1mpycodestyle \033[0m \n"; \
		pycodestyle --repeat --statistics --count --show-source $$PY_FOLDER || echo "failed, continue..."; \
		printf -- "\033[34;1misort \033[0m \n"; \
		isort --check-only --diff $$PY_FOLDER || echo "failed, continue..."; \
	done

.PHONY: lint-sec
lint-sec:
	@printf -- "\n\033[33;1m>>> Linting (security)... \033[0m\n"
	@for PY_FOLDER in $(PY_FOLDERS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		printf -- "\033[34;1mbandit \033[0m \n"; \
		bandit --recursive -s B101 $$PY_FOLDER || echo "failed, continue..."; \
		printf -- "\033[34;1msafety \033[0m \n"; \
		safety check || echo "failed, continue..."; \
	done

.PHONY: lint-pkg
lint-pkg:
	@printf -- "\n\033[33;1m>>> Linting (packaging)... \033[0m\n"
	@for PY_FOLDER in $(PY_FOLDERS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		printf -- "\033[34;1mcheck-manifest \033[0m \n"; \
		check-manifest -v || echo "failed, continue..."; \
	done

.PHONY: lint-type
lint-type:
	@printf -- "\n\033[33;1m>>> Linting (mypy)... \033[0m\n"
	@for PY_FOLDER in $(PY_FOLDERS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		printf -- "\033[34;1mmypy \033[0m \n"; \
		mypy $$PY_FOLDER || echo "failed, continue..."; \
	done

.PHONY: lint-docstring
lint-docstring:
	@printf -- "\n\033[33;1m>>> Linting (docstrings)... \033[0m\n"
	@for PY_FOLDER in $(PY_FOLDERS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		printf -- "\033[34;1mpydocstyle \033[0m \n"; \
		pydocstyle --explain --source --count $$PY_FOLDER || echo "failed, continue..."; \
		printf -- "\033[34;1mdarglint \033[0m \n"; \
		darglint --verbosity 2 --docstring-style numpy --strictness full $$PY_FOLDER || echo "failed, continue..."; \
	done

.PHONY: test
test:
	@printf -- "\n\033[33;1m>>> Test... \033[0m\n"
	@for PY_FOLDER_TEST in $(PY_FOLDERS_TESTS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		pytest $$PY_FOLDER_TEST; \
	done

.PHONY: test-v
test-v:
	@printf -- "\n\033[33;1m>>> Test... \033[0m\n"
	@for PY_FOLDER_TEST in $(PY_FOLDERS_TESTS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		pytest -v $$PY_FOLDER_TEST; \
	done

.PHONY: test-vv
test-vv:
	@printf -- "\n\033[33;1m>>> Test... \033[0m\n"
	@for PY_FOLDER_TEST in $(PY_FOLDERS_TESTS) ; do \
		printf -- "\033[36;1m$$PY_FOLDER... \033[0m \n"; \
		pytest -vv --capture=no $$PY_FOLDER_TEST; \
	done

.PHONY: clear-all
clear-all: clear-pyc clear-build

.PHONY: clear-pyc
clear-pyc:
	find . -type d -name '__pycache__' -not -path './venv/*' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -not -path './venv/*' -exec rm -f {} +
	find . -type f -name '*~' -not -path './venv/*' -exec rm -f {} +

.PHONY: clear-pybuild
clear-pybuild:
	rm -fr dist/
	rm -fr .eggs/
	rm -fr *.egg-info/
