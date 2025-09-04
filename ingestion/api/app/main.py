from fastapi import FastAPI
from .routers import transactions
from .fraud_features_http import router as features_router
api = FastAPI(title="Ingestion API")
api.include_router(transactions.router)
api.include_router(features_router)
fraud_api = api  # reuse port 8090 in docker CMD
