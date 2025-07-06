FROM python:3.12-slim

ARG POETRY_VERSION=1.8.5
ARG PIPX_VERSION=1.7.1
ARG APP_DIR=/opt/secunda_test_app

ENV PATH="/root/.local/bin:${PATH}" \
    APP_DIR="$APP_DIR" \
    PYTHONPATH="$APP_DIR:${PYTHONPATH-}"


RUN python -m pip install pipx=="$PIPX_VERSION" setuptools \
    && python -m pipx ensurepath \
    && pipx install poetry=="$POETRY_VERSION"

WORKDIR $APP_DIR

COPY backend ./backend
COPY migration ./migration
COPY alembic.ini ./alembic.ini
COPY .env ./env
COPY [ \
  "poetry.lock", \
  "pyproject.toml", \
  "./" \
]

RUN poetry config virtualenvs.create false && \
        poetry install --sync --no-root --no-interaction --without dev

EXPOSE 8000

CMD alembic -x data=true upgrade head && python backend/main.py