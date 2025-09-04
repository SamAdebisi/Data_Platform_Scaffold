FROM python:3.11-slim
WORKDIR /srv/app
COPY ingestion/api/pyproject.toml .
RUN pip install --no-cache-dir -e .
EXPOSE 8000 8090
CMD ["bash","-lc","uvicorn app.main:api --host 0.0.0.0 --port 8000 & uvicorn app.main:fraud_api --host 0.0.0.0 --port 8090 --reload"]
