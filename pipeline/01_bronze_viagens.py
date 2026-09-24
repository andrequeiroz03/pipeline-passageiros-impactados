from pyspark import pipelines as dp

bucket = "s3://meu-bucket-dados-json/raw/viagens/"

@dp.table
def bronze_viagens():
    df = (spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")
            .load(bucket)
    )   
    return df