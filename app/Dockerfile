FROM python:3.11-slim AS builder
WORKDIR /app

# Install build tools and if needed
RUN pip install -U pip 

# Copy only  dependencies definition first
COPY pyproject.toml /app/pyproject.toml

#Create venv and install runtime deps
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install -e .

#--------------------------------------------
#2) Test: install dev deps and run pytest
#--------------------------------------------
FROM builder AS test

WORKDIR /app
# Copy app source + tests
COPY src /app/src
COPY tests /app/tests
COPY pytest.ini /app/pytest.ini

COPY --from=builder /opt/venv /opt/venv

# Install dev deps
RUN /opt/venv/bin/pip install -U pip
RUN /opt/venv/bin/pip install -e . --group dev

# Run tests
RUN /opt/venv/bin/pytest


FROM python:3.11-slim AS runtime
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY src/ /app/src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

