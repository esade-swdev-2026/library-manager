FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md LICENSE ./
COPY src ./src
RUN uv sync --locked --no-dev

# data/ holds the committed books the app starts from, and it is the only folder the app
# writes to; a named volume on /app/data keeps the changes after the container is gone
RUN useradd --create-home app
COPY --chown=app:app data ./data
USER app

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["library-manager"]
CMD ["--help"]
