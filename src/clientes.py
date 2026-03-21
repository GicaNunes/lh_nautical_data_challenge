import pandas as pd

def run():
    print("=== Análise de Clientes rodando ===")

    vendas = pd.read_csv("data/csv/vendas_2023_2024.csv")
    produtos = pd.read_csv("data/csv/produtos_raw.csv")
    clientes = pd.read_json("data/json/clientes_crm.json")

    # Padronizar colunas
    vendas.columns = vendas.columns.str.lower()
    produtos.columns = produtos.columns.str.lower()
    clientes.columns = clientes.columns.str.lower()

    # Merge usando chaves corretas
    df = vendas.merge(produtos, left_on='id_product', right_on='code', how='left')
    df = df.merge(clientes, left_on='id_client', right_on='code', how='left')

    # Calcular lucro acumulado por cliente
    # Se não houver coluna de custo, usamos apenas o total
    if 'price' in produtos.columns:
        df['lucro'] = df['qtd'] * df['price']
    else:
        df['lucro'] = df['total']

    lucro_clientes = df.groupby('id_client')['lucro'].sum().sort_values(ascending=False)
    print(lucro_clientes.head())

    top_clientes = lucro_clientes.head(10)
    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("\n=== Clientes ===\n")
        f.write(str(top_clientes) + "\n")


if __name__ == "__main__":
    run()


