FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

CMD ["sh", "-c", "uv run streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT"]