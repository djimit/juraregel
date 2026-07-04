FROM python:3.14-slim
WORKDIR /app
COPY shared/ /app/shared/
COPY use-cases/ /app/use-cases/
COPY ci/ /app/ci/
RUN pip install fastapi uvicorn pydantic jsonschema pytest httpx
EXPOSE 8490-8497
