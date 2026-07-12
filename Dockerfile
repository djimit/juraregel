FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home juraregel
COPY --chown=juraregel:juraregel shared/ shared/
COPY --chown=juraregel:juraregel use-cases/ use-cases/

USER juraregel
EXPOSE 8490 8493
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8490/v1/health')"
CMD ["uvicorn", "app:app", "--app-dir", "use-cases/griffierecht/api", "--host", "0.0.0.0", "--port", "8490"]
