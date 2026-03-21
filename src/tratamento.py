import pandas as pd


def run():
    print("=== Tratamento rodando ===")

    vendas = pd.read_csv("data/csv/vendas_2023_2024.csv")
    produtos = pd.read_csv("data/csv/produtos_raw.csv")
    clientes = pd.read_json("data/json/clientes_crm.json")

    # Padronizar nomes
    vendas.columns = vendas.columns.str.lower()
    produtos.columns = produtos.columns.str.lower()
    clientes.columns = clientes.columns.str.lower()

    # Padronizar datas
    vendas['sale_date'] = pd.to_datetime(vendas['sale_date'], errors='coerce')

    # Remover duplicados
    vendas = vendas.drop_duplicates()

    # Normalizar nomes de produtos
    produtos['name'] = produtos['name'].str.strip().str.lower()

    # Merge usando chaves corretas
    df = vendas.merge(produtos, left_on='id_product', right_on='code', how='left')
    df = df.merge(clientes, left_on='id_client', right_on='code', how='left')

    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("\n=== Tratamento ===\n")
        f.write("Dataframe tratado salvo em data/df_tratado.csv\n")
        f.write("Colunas finais: " + str(df.columns.tolist()) + "\n")
        f.write("Total de registers: " + str(len(df)) + "\n")

    print(df.head())
    return df

if __name__ == "__main__":
    run()
