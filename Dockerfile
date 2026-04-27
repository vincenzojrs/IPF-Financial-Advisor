# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_CODE=copy

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY ./ /app

ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN /app/.venv/bin/playwright install chromium

ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT"]