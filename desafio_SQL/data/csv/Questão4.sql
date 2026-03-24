WITH vendas_custo AS (
    SELECT 
        v.id_product,
        v.sale_date,
        v.qtd,
        v.total AS valor_venda_brl,
        c.custo_usd,
        x.taxa_cambio,
        -- custo unitário convertido para BRL
        (c.custo_usd * x.taxa_cambio) AS custo_unitario_brl,
        -- custo total da transação em BRL
        (v.qtd * c.custo_usd * x.taxa_cambio) AS custo_total_brl,
        -- prejuízo da transação (se houver)
        CASE 
            WHEN v.total < (v.qtd * c.custo_usd * x.taxa_cambio) 
            THEN ( (v.qtd * c.custo_usd * x.taxa_cambio) - v.total )
            ELSE 0
        END AS prejuizo_brl
    FROM vendas_2023_2024 v
    INNER JOIN custos_importacao c 
        ON v.id_product = c.id_product
    INNER JOIN cambio_diario x 
        ON substr(v.sale_date, 1, 10) = x.data
)
SELECT 
    id_product,
    SUM(valor_venda_brl) AS receita_total_brl,
    SUM(prejuizo_brl) AS prejuizo_total_brl,
    ROUND(SUM(prejuizo_brl) * 1.0 / SUM(valor_venda_brl), 4) AS percentual_perda
FROM vendas_custo
GROUP BY id_product
HAVING SUM(prejuizo_brl) > 0
ORDER BY percentual_perda DESC;
