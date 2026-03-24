import pandas as pd
import json

# Carregar o arquivo JSON
with open("../data/json/custos_importacao.json", "r", encoding="utf-8") as f:
    data = json.load(f)

linhas = []
for produto in data:
    for preco in produto.get("prices", []):
        # Detecta automaticamente os nomes das chaves
        # Se não existir 'start_date', tenta 'date' ou 'inicio'
        data_chave = preco.get("start_date") or preco.get("date") or preco.get("inicio")
        preco_chave = preco.get("usd_price") or preco.get("price") or preco.get("valor")

        linhas.append({
            "product_id": produto.get("product_id"),
            "product_name": produto.get("product_name"),
            "category": produto.get("category"),
            "start_date": data_chave,
            "usd_price": preco_chave
        })

# Criar DataFrame
df = pd.DataFrame(linhas)

# Converter tipos
if "start_date" in df.columns:
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
if "usd_price" in df.columns:
    df["usd_price"] = pd.to_numeric(df["usd_price"], errors="coerce")

# Remover duplicatas
df = df.drop_duplicates()

# Salvar em CSV
df.to_csv("../data/csv/custos_importacao.csv", index=False)

print("Arquivo custos_importacao.csv gerado com sucesso!")
