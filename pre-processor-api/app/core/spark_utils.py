from pyspark.sql import SparkSession
from app.core.config import settings

def get_spark_session(app_name: str = "DataPreprocessingApp") -> SparkSession:
    """
    Inicializa e retorna uma sessão Spark configurada para se conectar ao MinIO.
    """
    spark = SparkSession.builder.appName(app_name).master("local[*]") \
        .config("spark.hadoop.fs.s3a.endpoint", settings.MINIO_ENDPOINT) \
        .config("spark.hadoop.fs.s3a.access.key", settings.MINIO_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", settings.MINIO_SECRET_KEY) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.367") \
        .config("spark.hadoop.fs.s3a.threads.keepalivetime", "60000") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.hadoop.fs.s3a.connection.establish.timeout", "5000") \
        .config("spark.hadoop.fs.s3a.connection.timeout", "50000") \
        .config("spark.hadoop.fs.s3a.readahead.range", "2097152") \
        .config("spark.hadoop.fs.s3a.socket.recv.buffer", "65536") \
        .config("spark.hadoop.fs.s3a.socket.send.buffer", "65536") \
        .config("spark.hadoop.fs.s3a.multipart.threshold", "20971520") \
        .config("spark.hadoop.fs.s3a.fast.upload.buffer", "disk") \
        .config("spark.hadoop.fs.s3a.fast.upload.active.blocks", "4") \
        .config("spark.hadoop.fs.s3a.fast.upload.active.multiparts", "4") \
        .config("spark.hadoop.fs.s3a.impl.disable.cache", "true") \
        .config("spark.hadoop.fs.s3a.paging.maximum", "1000") \
        .config("spark.hadoop.fs.s3a.list.version", "2") \
        .config("spark.hadoop.fs.s3a.max.total.data.connections", "200") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.attempts", "5") \
        .config("spark.hadoop.fs.s3a.multipart.purge.age", "86400") \
        .getOrCreate()
    return spark