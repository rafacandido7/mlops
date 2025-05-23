from fastapi import FastAPI
from app.api.endpoints import data_processing 

app = FastAPI(
    title="Spark Data Preprocessing API",
    description="API para orquestrar o pré-processamento de dados com PySpark e MinIO.",
    version="1.0.0"
)

app.include_router(data_processing.router, prefix="/api/v1", tags=["Data Processing"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Processamento de Dados Spark! Acesse /docs para a documentação interativa."}