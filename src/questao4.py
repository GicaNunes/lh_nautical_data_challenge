import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# -----------------------------
# Parte 1 — Baixar câmbio diário
# -----------------------------
data_inicial = "01/01/2023"
data_final = datetime.today().strftime("%d/%m/%Y")

url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    cambio = pd.DataFrame(data)
    cambio.rename(columns={"data": "date", "valor": "usd_brl"}, inplace=True)
    cambio["date"] = pd.to_datetime(cambio["date"], dayfirst=True)
    cambio["usd_brl"] = pd.to_numeric(cambio["usd_brl"], errors="coerce")
else:
    raise Exception(f"Erro ao baixar câmbio: {response.status_code}")

# -----------------------------
# Parte 2 — Carregar datasets
# -----------------------------
vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")
custos = pd.read_csv("../data/csv/custos_importacao.csv")

print("Colunas em vendas:", vendas.columns.tolist())
print("Colunas em custos:", custos.columns.tolist())

# Converter datas
vendas["sale_date"] = pd.to_datetime(vendas["sale_date"], errors="coerce", dayfirst=True)
if "start_date" in custos.columns:
    custos["start_date"] = pd.to_datetime(custos["start_date"], errors="coerce", dayfirst=True)

# -----------------------------
# Parte 3 — Cruzar dados
# -----------------------------
# Juntar câmbio na venda
vendas = vendas.merge(cambio, left_on="sale_date", right_on="date", how="left")

# Juntar custos usando id_product (vendas) e product_id (custos)
vendas = vendas.merge(custos[["product_id", "product_name", "usd_price"]],
                      left_on="id_product", right_on="product_id", how="left")

# -----------------------------
# Parte 4 — Cálculos
# -----------------------------
vendas["custo_total_brl"] = vendas["qtd"] * (vendas["usd_price"] * vendas["usd_brl"])
vendas["prejuizo"] = (vendas["custo_total_brl"] - vendas["total"]).clip(lower=0)

# -----------------------------
# Parte 5 — Agregar por produto
# -----------------------------
df_agregado = vendas.groupby(["product_id", "product_name"]).agg(
    receita_total=("total", "sum"),
    prejuizo_total=("prejuizo", "sum")
).reset_index()

df_agregado["percentual_perda"] = df_agregado["prejuizo_total"] / df_agregado["receita_total"]

# -----------------------------
# -----------------------------
# Parte 6 — Gráfico (horizontal com todos os produtos)
# -----------------------------
df_prejuizo = df_agregado[df_agregado["prejuizo_total"] > 0]

plt.figure(figsize=(12, 18))  # altura maior para caber todos os nomes
plt.barh(df_prejuizo["product_name"], df_prejuizo["prejuizo_total"], color="red")
plt.xlabel("Prejuízo Total (BRL)")
plt.title("Prejuízo por Produto")
plt.tight_layout()
plt.show()

# -----------------------------
# Parte 8 — Produto com maior percentual de perda
# -----------------------------
produto_maior_perda = df_agregado.loc[df_agregado["percentual_perda"].idxmax()]

print("\n=== Produto com maior percentual de perda ===")
print(f"ID Produto: {produto_maior_perda['product_id']}")
print(f"Nome Produto: {produto_maior_perda['product_name']}")
print(f"Receita Total: R$ {produto_maior_perda['receita_total']:,.2f}")
print(f"Prejuízo Total: R$ {produto_maior_perda['prejuizo_total']:,.2f}")
print(f"Percentual de Perda: {produto_maior_perda['percentual_perda']:.2%}")



# -----------------------------
# Parte 7 — Exportar resumo
# -----------------------------
df_agregado.to_csv("../data/csv/resumo_prejuizos.csv", index=False)
print("Resumo salvo em resumo_prejuizos.csv")

