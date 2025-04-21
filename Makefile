SHELL := /bin/bash

# Default target
.PHONY: all
all: run

# Install all Python dependencies using uv
install:
	@command -v uv >/dev/null 2>&1 || { \
	  echo "uv is not installed. Installing uv..."; \
	  curl -LsSf https://astral.sh/uv/latest/install.sh | sh; \
	  source ~/.bashrc; \
	}
	uv sync --dev --extra jupyter --frozen

# Run unit and integration tests
test:
	uv run pytest tests/unit
test-integration:
	uv run pytest tests/integration

# Launch Streamlit playground
playground:
	uv run adk web

# Deploy backend via Terraform
backend:
	make setup-dev-env
	terraform apply -var="project=$(PROJECT)" deployment/

# Set up dev environment resources using Terraform
setup-dev-env:
	gcloud config set project $(PROJECT)
	terraform init deployment/
	terraform apply -var="project=$(PROJECT)" deployment/

# Code quality checks
lint:
	uv run codespell
	uv run ruff . --diff
	uv run ruff format . --check --diff
	uv run mypy .

# Start Flask against your deployed (remote) engine
run:
	. .venv/bin/activate && \
	export USE_REMOTE=true && \
	fuser -k 8080/tcp 2>/dev/null || true && \
	python3 app/agent_engine_app.py

# Dev mode: stub agent + React hot-reload
run-dev:
	. .venv/bin/activate && \
	export USE_REMOTE=false && \
	fuser -k 8080/tcp 2>/dev/null || true && \
	python3 app/agent_engine_app.py & \
	cd frontend && \
	export HOST=0.0.0.0 PORT=3001 && \
	npm start
