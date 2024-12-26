FROM python:3.12

WORKDIR /app

RUN pip install uv
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync
COPY . .

CMD uv run main.py