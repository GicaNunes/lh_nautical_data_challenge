import pandas as pd


df = pd.read_csv("../data/csv/produtos_raw.csv")

# --- Parte 1: Padronizar categorias ---
df['actual_category'] = df['actual_category'].str.lower()

mapa_categorias = {
    'eletronicos': 'eletrônicos',
    'eletronico': 'eletrônicos',
    'propulsao': 'propulsão',
    'propulsor': 'propulsão',
    'ancoragem': 'ancoragem',
    'ancora': 'ancoragem'
}
df['actual_category'] = df['actual_category'].replace(mapa_categorias)

# --- Parte 2: Converter valores para numérico ---
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# --- Parte 3: Remover duplicatas ---
df = df.drop_duplicates()

# Salvar resultado final
df.to_csv("../data/csv/produtos_normalizados.csv", index=False)

print("Normalização concluída! Arquivo salvo em produtos_normalizados.csv")
