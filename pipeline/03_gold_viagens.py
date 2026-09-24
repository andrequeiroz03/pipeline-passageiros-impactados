from pyspark import pipelines as dp
from pyspark.sql.window import Window
from pyspark.sql.functions import col, date_format, row_number, regexp_extract, regexp_replace, lag, unix_timestamp

@dp.table
def gold_viagens():
    df = spark.read.table("passageiros_impactados.dados.silver_viagens")

    df = df.filter(
        (col("status") == "Concluída") &
        (col("row_num") == 1) &
        (col("prefixo_letras").isin("F", "J")) &
        (col("sigla_estacao") == "BFU") &
        (col("partida_realizada").between("04:00:00", "23:59:59"))
    )

    window_spec = Window.partitionBy("data_referencia").orderBy("partida_realizada")
    df = ( 
        df
        .withColumn("partida_anterior", lag("partida_realizada").over(window_spec))
        .withColumn("headway", unix_timestamp(col("partida_realizada"), "HH:mm:ss") - unix_timestamp(col("partida_anterior"), "HH:mm:ss"))
    )

    df = df.select(
        "data_referencia",
        "prefixo",
        "prefixo_letras",
        "sigla_estacao",
        "partida_realizada",
        "partida_anterior",
        "headway"
    )

    return df