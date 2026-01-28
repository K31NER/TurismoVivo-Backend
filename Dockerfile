FROM python:3.11-slim AS builder

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]