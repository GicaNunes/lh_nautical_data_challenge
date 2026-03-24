import pandas as pd

# Carregar dataset
df = pd.read_csv("../data/csv/vendas_2023_2024.csv")

# Converter datas
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

# Parte 1 — Visão geral
print("Quantidade de linhas:", df.shape[0])
print("Quantidade de colunas:", df.shape[1])
print("Data mínima:", df['sale_date'].min())
print("Data máxima:", df['sale_date'].max())

# Parte 2 — Estatísticas da coluna 'total'
print("Valor mínimo:", df['total'].min())
print("Valor máximo:", df['total'].max())
print("Valor médio:", df['total'].mean())
