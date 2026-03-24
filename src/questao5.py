import pandas as pd

# -----------------------------
# Parte 1 — Carregar datasets
# -----------------------------
vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")
produtos = pd.read_csv("../data/csv/produtos_raw.csv")

print("Colunas em produtos:", produtos.columns.tolist())

# -----------------------------
# Parte 2 — Limpeza das categorias
# -----------------------------
mapa_categorias = {
    "Ancorajen": "Ancoragem",
    "Encoragem": "Ancoragem",
    "Ancoragem": "Ancoragem",
    # incluir outros ajustes conforme necessário
}

produtos["category_clean"] = produtos["actual_category"].replace(mapa_categorias)

# -----------------------------
# Parte 3 — Juntar vendas com produtos
# -----------------------------
# Aqui usamos 'code' (produtos) ↔ 'id_product' (vendas)
vendas = vendas.merge(produtos[["code", "category_clean"]],
                      left_on="id_product", right_on="code", how="left")

# -----------------------------
# Parte 4 — Métricas por cliente
# -----------------------------
clientes = vendas.groupby("id_client").agg(
    faturamento_total=("total", "sum"),
    frequencia=("id", "count"),
    diversidade_categorias=("category_clean", "nunique")
).reset_index()

clientes["ticket_medio"] = clientes["faturamento_total"] / clientes["frequencia"]

# -----------------------------
# Parte 5 — Filtro de elite
# -----------------------------
clientes_elite = clientes[clientes["diversidade_categorias"] >= 3]
clientes_elite = clientes_elite.sort_values(
    by=["ticket_medio", "id_client"], ascending=[False, True]
).head(10)

print("\n=== Top 10 Clientes de Elite ===")
print(clientes_elite)

# -----------------------------
# Parte 6 — Categoria mais consumida pelos clientes de elite
# -----------------------------
vendas_elite = vendas[vendas["id_client"].isin(clientes_elite["id_client"])]
categoria_top = vendas_elite.groupby("category_clean")["qtd"].sum().reset_index()
categoria_top = categoria_top.sort_values("qtd", ascending=False).head(1)

print("\n=== Categoria mais consumida pelos clientes de elite ===")
print(categoria_top)

# -----------------------------
# Parte 8 — Validação (Questão 5.2)
# -----------------------------
# Filtrar vendas apenas dos Top 10 clientes fiéis
vendas_top10 = vendas[vendas["id_client"].isin(clientes_elite["id_client"])]

# Somar quantidade de itens por categoria
categoria_valida = vendas_top10.groupby("category_clean")["qtd"].sum().reset_index()

# Ordenar para pegar a categoria mais vendida
categoria_valida = categoria_valida.sort_values("qtd", ascending=False).head(1)

print("\n=== Questão 5.2 — Categoria mais vendida para os Top 10 clientes fiéis ===")
print(categoria_valida)

