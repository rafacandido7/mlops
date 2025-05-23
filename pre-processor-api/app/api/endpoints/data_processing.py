from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.data_processor import DataProcessor
import os

router = APIRouter()

@router.post("/process-csv-upload/")
async def process_csv_upload(file: UploadFile = File(...)):
    """
    Endpoint para fazer upload de um arquivo CSV, pré-processar com Spark e salvar no MinIO.
    O arquivo é salvo temporariamente no disco para processamento robusto de grandes volumes.
    """
    if not file.filename.lower().endswith('.csv'): 
        raise HTTPException(status_code=400, detail="O arquivo deve ser do tipo .csv")

    try:
        processor = DataProcessor()
        result = processor.preprocess_and_save_data(file.file)

        if result["status"] == "success":
            return {"message": "Data uploaded to s3!", "output_path": result["output_path"]}
        else:
            raise HTTPException(status_code=500, detail=f"Falha no processamento: {result['message']}")
    except Exception as e:
        print(f"Erro no endpoint /process-csv-upload/: {e}", exc_info=True) 
        raise HTTPException(status_code=500, detail=f"Erro inesperado no servidor. Por favor, tente novamente mais tarde. Detalhe: {str(e)}")
    finally:
        await file.close()