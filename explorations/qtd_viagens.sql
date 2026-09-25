SELECT
    data_referencia,
    COUNT(*) AS qtd_viagens

FROM passageiros_impactados.dados.gold_viagens

GROUP BY data_referencia