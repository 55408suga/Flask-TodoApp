FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen 
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 5000
CMD ["flask", "run","--host","0.0.0.0"]