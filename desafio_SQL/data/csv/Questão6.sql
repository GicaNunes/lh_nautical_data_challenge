

-- 1. Criar calendário entre a menor e a maior data de venda
WITH RECURSIVE calendario AS (
    SELECT MIN(date(sale_date)) AS data
    FROM vendas_2023_2024
    UNION ALL
    SELECT date(data, '+1 day')
    FROM calendario
    WHERE data < (SELECT MAX(date(sale_date)) FROM vendas_2023_2024)
),

-- 2. Adicionar dia da semana em português
calendario_semana AS (
    SELECT 
        data,
        CASE strftime('%w', data)
            WHEN '0' THEN 'Domingo'
            WHEN '1' THEN 'Segunda-feira'
            WHEN '2' THEN 'Terça-feira'
            WHEN '3' THEN 'Quarta-feira'
            WHEN '4' THEN 'Quinta-feira'
            WHEN '5' THEN 'Sexta-feira'
            WHEN '6' THEN 'Sábado'
        END AS dia_semana
    FROM calendario
),

-- 3. Vendas diárias (soma por dia)
vendas_diarias AS (
    SELECT 
        date(sale_date) AS data,
        SUM(CAST(total AS REAL)) AS valor_venda
    FROM vendas_2023_2024
    GROUP BY date(sale_date)
)

-- 4. Juntar calendário com vendas (dias sem venda = 0)
SELECT 
    c.dia_semana,
    AVG(COALESCE(v.valor_venda, 0)) AS media_vendas
FROM calendario_semana c
LEFT JOIN vendas_diarias v 
    ON c.data = v.data
GROUP BY c.dia_semana
ORDER BY media_vendas ASC;
