

-- Quantidade total de linhas
SELECT COUNT(*) AS total_linhas
FROM vendas_2023_2024;

-- Quantidade total de colunas
SELECT COUNT(*) AS total_colunas
FROM pragma_table_info('vendas_2023_2024');

-- Intervalo de datas analisado
SELECT MIN(sale_date) AS data_min,
       MAX(sale_date) AS data_max
FROM vendas_2023_2024;

-- Estatísticas de valores
SELECT MIN(total) AS valor_min,
       MAX(total) AS valor_max,
       AVG(total) AS valor_medio
FROM vendas_2023_2024;
