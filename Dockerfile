FROM python:3.12-slim AS builder
WORKDIR /app
COPY shared/ /app/shared/
COPY use-cases/ /app/use-cases/
RUN pip install --no-cache-dir fastapi uvicorn pydantic jsonschema pyyaml httpx pytest

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/ /app/
RUN useradd -m juraregel
USER juraregel
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8490/v1/health')" || exit 1
EXPOSE 8490-8515
CMD ["python3", "use-cases/griffierecht/api/app.py"]
