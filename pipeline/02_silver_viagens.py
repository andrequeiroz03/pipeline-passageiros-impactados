from pyspark import pipelines as dp
from pyspark.sql.window import Window
from pyspark.sql.functions import col, date_format, row_number, regexp_extract, regexp_replace

@dp.table
def silver_viagens():
    df = spark.read.table("passageiros_impactados.dados.bronze_viagens")

    #selecionar colunas
    df =  df.select(
        col("data_referencia"),
        col("prefixo"),
        regexp_extract(col("prefixo"), r"^([A-Za-z]+)", 1).alias("prefixo_letras"),
        regexp_replace(col("status"), "ConcluÃ­da", "Concluída").alias("status"),
        col("tipo_viagem"),
        col("sigla_estacao"),
        date_format(col("partida_realizada"), "HH:mm:ss").alias("partida_realizada")
    )

    #definir pontos de partida do trem
    window_spec = Window.partitionBy("data_referencia", "prefixo").orderBy("partida_realizada")
    df = df.withColumn("row_num", row_number().over(window_spec))

    #ordenar as viagens para facilitar visualização 
    df = df.orderBy(
        "data_referencia",
        "prefixo",
        "partida_realizada"
    )

    return df