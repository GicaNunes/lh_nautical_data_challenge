import pandas as pd
import json

# Carregar JSON
with open("../data/json/custos_importacao.json", "r", encoding="utf-8") as f:
    data = json.load(f)

linhas = []
for produto in data:
    for preco in produto.get("historic_data", []):  # <-- ajuste aqui
        linhas.append({
            "product_id": produto.get("product_id"),
            "product_name": produto.get("product_name"),
            "category": produto.get("category"),
            "start_date": preco.get("start_date"),
            "usd_price": preco.get("usd_price")
        })

# Criar DataFrame
df = pd.DataFrame(linhas)

# Converter tipos
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce", dayfirst=True)
df["usd_price"] = pd.to_numeric(df["usd_price"], errors="coerce")

# Remover duplicatas
df = df.drop_duplicates()

# Contar entradas finais
print("Total de entradas de importação após normalização:", df.shape[0])

# Salvar CSV
df.to_csv("../data/csv/custos_importacao.csv", index=False)

print("Arquivo custos_importacao.csv gerado com sucesso!")
