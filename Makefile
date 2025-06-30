##@ Lint
.PHONY: lint.mypy
lint.mypy: ## Run mypy
	@mypy --sqlite-cache

.PHONY: lint.flake8
lint.flake8: ## Run flake8
	@flake8

.PHONY: lint.isort
lint.isort: ## Run isort check only
	@isort --check-only --diff .

.PHONY: lint.black
lint.black: ## Run black check only
	@black --check --diff .

.PHONY: lint.fix
lint.fix: ## Run linters auto fix flake8, isort, black
	autoflake --in-place -r . && isort . && black .
