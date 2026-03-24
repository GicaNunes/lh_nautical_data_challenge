import pandas as pd
from sklearn.metrics import mean_absolute_error

# 1. Ler dataset
vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")

# 2. Descobrir qual ID corresponde ao produto desejado
print(vendas[["id_product"]].drop_duplicates())

# Suponha que o ID do "Motor de Popa Yamaha Evo Dash 155HP" seja 105
produto = vendas[vendas["id_product"] == 105].copy()

# 3. Converter datas
produto["sale_date"] = pd.to_datetime(produto["sale_date"], errors="coerce")

# 4. Agregar vendas por dia
diario = produto.groupby("sale_date")["qtd"].sum().reset_index()

# 5. Separar treino e teste
treino = diario[diario["sale_date"] <= pd.to_datetime("2023-12-31")].copy()
teste = diario[(diario["sale_date"] >= pd.to_datetime("2024-01-01")) &
               (diario["sale_date"] <= pd.to_datetime("2024-01-31"))].copy()

print("Linhas treino:", len(treino))
print("Linhas teste:", len(teste))

if teste.empty:
    print("Não há dados de vendas para Janeiro/2024. O baseline não pode ser avaliado.")
else:
    previsoes = []
    for data in teste["sale_date"]:
        historico = diario[diario["sale_date"] < data]
        previsao = historico["qtd"].tail(7).mean()
        previsoes.append(previsao)

    teste["previsao"] = previsoes
    mae = mean_absolute_error(teste["qtd"], teste["previsao"])
    print("MAE (Janeiro/2024):", round(mae, 2))
