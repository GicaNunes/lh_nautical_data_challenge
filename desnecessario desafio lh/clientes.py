import pandas as pd
from errors import FileProcessingError, DataValidationError, BusinessLogicError, log_error

def run():
    print("=== Análise de Clientes rodando ===")

    try:
        # Carregar datasets
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
        if 'price' in produtos.columns:
            df['lucro'] = df['qtd'] * df['price']
        elif 'total' in df.columns:
            df['lucro'] = df['total']
        else:
            raise BusinessLogicError("Não foi possível calcular lucro: coluna 'price' ou 'total' ausente.")

        lucro_clientes = df.groupby('id_client')['lucro'].sum().sort_values(ascending=False)
        print(lucro_clientes.head())

        # Salvar top clientes em arquivo
        top_clientes = lucro_clientes.head(10)
        with open("resultados.txt", "a", encoding="utf-8") as f:
            f.write("\n=== Clientes ===\n")
            f.write(str(top_clientes) + "\n")

    except FileNotFoundError as e:
        log_error(FileProcessingError(f"Arquivo não encontrado: {e}"))
        print("Erro: algum arquivo CSV/JSON não foi encontrado.")
    except BusinessLogicError as e:
        log_error(e)
        print("Erro de lógica:", e)
    except Exception as e:
        log_error(e)
        print("Erro inesperado:", e)

if __name__ == "__main__":
    run()
