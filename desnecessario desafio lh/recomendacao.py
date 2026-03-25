import pandas as pd

def run():
    print("=== Sistema de Recomendação rodando ===")

    produtos = pd.read_csv("data/csv/produtos_raw.csv")
    vendas = pd.read_csv("data/csv/vendas_2023_2024.csv")

    # Padronizar colunas
    produtos.columns = produtos.columns.str.lower()
    vendas.columns = vendas.columns.str.lower()

    # Função de recomendação por categoria
    def recomendar_por_categoria(produto_code):
        categoria = produtos.loc[produtos['code'] == produto_code, 'actual_category'].values[0]
        recomendados = produtos[produtos['actual_category'] == categoria]['name'].unique()
        return recomendados

    # Exemplo: recomendação para o produto com code = 1
    print("Exemplo recomendação por categoria:", recomendar_por_categoria(1))

    # Colaborativo simples: produtos mais vendidos
    top_produtos = vendas.groupby('id_product')['qtd'].sum().sort_values(ascending=False).head(5)
    print("Produtos mais populares (codes):", top_produtos.index.tolist())

if __name__ == "__main__":
    run()
