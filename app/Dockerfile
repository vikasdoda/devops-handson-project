FROM python:3.11-slim AS builder
WORKDIR /app

# Install build tools and if needed
RUN pip install -U pip

# Copy only  dependencies definition first
COPY pyproject.toml /app/pyproject.toml

#Create venv and install runtime deps
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install -e .



FROM python:3.11-slim AS runtime
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY src/ /app/src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

