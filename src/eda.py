import pandas as pd

def run():
    print("=== EDA rodando ===")

    produtos = pd.read_csv("data/csv/produtos_raw.csv")
    vendas = pd.read_csv("data/csv/vendas_2023_2024.csv")
    clientes = pd.read_json("data/json/clientes_crm.json")

    print("\nProdutos:")
    print(produtos.info())
    print("\nVendas:")
    print(vendas.describe())
    print("\nClientes:")
    print(clientes.head())

    resumo = produtos.describe()  # ou qualquer análise que você fez
    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("\n=== EDA ===\n")
        f.write(str(resumo) + "\n")

if __name__ == "__main__":
    run()



