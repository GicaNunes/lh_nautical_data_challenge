

WITH categorias_limpa AS (
    SELECT 
        p.product_id,
        CASE 
            WHEN LOWER(TRIM(p.category)) IN ('ancorajem','encoragem','ancoragem') THEN 'ancoragem'
            WHEN LOWER(TRIM(p.category)) IN ('eletronicos','eletrônico','eletrônicos') THEN 'eletrônicos'
            WHEN LOWER(TRIM(p.category)) IN ('propulsao','propulsor','propulsão') THEN 'propulsão'
            ELSE LOWER(TRIM(p.category))
        END AS categoria_padronizada
    FROM produtos_raw p
),

vendas_clientes AS (
    SELECT 
        v.id_client,
        v.id AS id_venda,
        v.id_product,
        CAST(v.qtd AS INTEGER) AS qtd,
        CAST(v.total AS REAL) AS total,
        c.categoria_padronizada
    FROM vendas_2023_2024 v
    JOIN categorias_limpa c 
        ON v.id_product = c.product_id
),

metricas_clientes AS (
    SELECT 
        id_client,
        SUM(total) AS faturamento_total,
        COUNT(DISTINCT id_venda) AS frequencia,
        SUM(total) * 1.0 / COUNT(DISTINCT id_venda) AS ticket_medio,
        COUNT(DISTINCT categoria_padronizada) AS diversidade_categorias
    FROM vendas_clientes
    GROUP BY id_client
),

clientes_fieis AS (
    SELECT 
        id_client,
        ticket_medio,
        diversidade_categorias
    FROM metricas_clientes
    WHERE diversidade_categorias >= 3
    ORDER BY ticket_medio DESC, id_client ASC
    LIMIT 10
)

SELECT 
    vc.categoria_padronizada,
    SUM(vc.qtd) AS total_itens
FROM vendas_clientes vc
JOIN clientes_fieis cf 
    ON vc.id_client = cf.id_client
GROUP BY vc.categoria_padronizada
ORDER BY total_itens DESC
LIMIT 1;
