FROM python:3.12.1-slim

WORKDIR /app

COPY . /app

RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [".venv/bin/python", "main.py"]