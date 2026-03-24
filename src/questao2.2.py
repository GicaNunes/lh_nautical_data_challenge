import pandas as pd

# Carregar dataset bruto
df = pd.read_csv("../data/csv/produtos_raw.csv")

# Contar linhas originais
linhas_originais = df.shape[0]

# Verificar se existe a coluna 'categoria'
if "categoria" in df.columns:
    df["categoria"] = df["categoria"].str.strip().str.lower()
    mapa_categorias = {
        "eletronicos": "eletrônicos",
        "eletrônico": "eletrônicos",
        "propulsao": "propulsão",
        "propulsor": "propulsão",
        "ancoragem": "ancoragem",
        "ancora": "ancoragem"
    }
    df["categoria"] = df["categoria"].replace(mapa_categorias)
else:
    print("⚠️ A coluna 'categoria' não existe no CSV. Verifique o nome correto com df.columns.")

# Converter valores para numérico (se existir coluna 'valor')
if "valor" in df.columns:
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

# Remover duplicatas
df_limpo = df.drop_duplicates()

# Contar linhas após limpeza
linhas_final = df_limpo.shape[0]
duplicatas_removidas = linhas_originais - linhas_final

print(f"Produtos duplicados removidos: {duplicatas_removidas}")
