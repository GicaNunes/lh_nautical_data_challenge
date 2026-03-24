import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# 1. Ler dataset
vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")

# 2. Construir matriz usuário–item (presença/ausência)
matriz = vendas.groupby(["id_client", "id_product"]).size().unstack(fill_value=0)
matriz = (matriz > 0).astype(int)

# 3. Calcular similaridade de cosseno entre produtos
similaridade = cosine_similarity(matriz.T)
sim_df = pd.DataFrame(similaridade,
                      index=matriz.columns,
                      columns=matriz.columns)

# 4. Ranking de produtos similares ao GPS
# Se id_product for numérico, substitua pelo ID correto do GPS
produto_ref = 105  # exemplo: ID do "GPS Garmin Vortex Maré Drift"

ranking = sim_df[produto_ref].drop(produto_ref).sort_values(ascending=False).head(5)
print("Top 5 produtos similares ao", produto_ref)
print(ranking)

