from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import time
import io
import os 
from app.core.config import settings
from app.core.spark_utils import get_spark_session

class DataProcessor:
    def __init__(self):
        self.spark = get_spark_session()
        self.minio_bucket_name = settings.MINIO_BUCKET_NAME

    def preprocess_and_save_data(self, file_stream: io.BytesIO):
        """
        Lê um arquivo CSV via stream, salva temporariamente no disco,
        preprocessa os dados com Spark e salva em formato Parquet no MinIO.

        Args:
            file_stream (io.BytesIO): Um objeto stream do arquivo CSV enviado via upload.
        """
        temp_csv_path = None 
        try:
            temp_csv_path = f"/tmp/uploaded_cpu_data_{int(time.time())}_{os.getpid()}.csv"

            with open(temp_csv_path, "wb") as f:
                while True:
                    chunk = file_stream.read(8192) 
                    if not chunk:
                        break
                    f.write(chunk)

            print(f"Arquivo CSV temporário salvo em: {temp_csv_path}")
            print(f"Lendo arquivo CSV do disco para o Spark: {temp_csv_path}")

            df_spark = self.spark.read.csv(temp_csv_path, header=True, inferSchema=True)

            print("Schema do DataFrame original:")
            df_spark.printSchema()

            df_spark = df_spark.withColumn("MMAX_numeric", col("MMAX").cast("integer")) \
                               .withColumn("MMIN_numeric", col("MMIN").cast("integer"))

            df_spark = df_spark.filter(col("MMAX_numeric") <= 30000)
            df_spark = df_spark.filter(col("MMIN_numeric") <= 10000)

            if df_spark.count() == 0:
                print("Nenhuma linha restou após a filtragem. Verifique os filtros ou os dados de entrada.")
                return {"status": "failure", "message": "Nenhuma linha restou após a filtragem."}

            columns_to_drop = ['vendor', 'MMAX_numeric', 'MMIN_numeric']
            actual_columns_to_drop = [c for c in columns_to_drop if c in df_spark.columns]
            df_processed = df_spark.drop(*actual_columns_to_drop)

            parquet_object_name = f"clean_data/cpu-data-{int(time.time())}.parquet"
            output_path_s3a = f"s3a://{self.minio_bucket_name}/{parquet_object_name}"

            print(f"\nIniciando upload (escrita) para o MinIO em: {output_path_s3a}")
            df_processed.write.mode("overwrite").parquet(output_path_s3a)
            print(f"DataFrame 'df_processed' salvo com sucesso no MinIO em '{output_path_s3a}'")

            return {"status": "success", "output_path": output_path_s3a}

        except Exception as e:
            print(f"Erro no processamento de dados Spark: {e}")
            return {"status": "failure", "message": str(e)}
        finally:
            self.spark.stop()
            if temp_csv_path and os.path.exists(temp_csv_path):
                try:
                    os.remove(temp_csv_path)
                    print(f"Arquivo temporário {temp_csv_path} removido.")
                except OSError as e:
                    print(f"Erro ao remover arquivo temporário {temp_csv_path}: {e}")