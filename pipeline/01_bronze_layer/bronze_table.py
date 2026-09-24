from pyspark import pipelines as dp

bucket = "s3://meu-bucket-dados-json/raw/partidas_trem/"

@dp.table(
    name="workspace.andre_testes.bronze_table"
)
def bronze_table():
    df = (spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")
            .load(bucket)
    )   
    return df