import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from errors import DataValidationError, FileProcessingError, log_error

def recomendar_produtos():
    try:
        vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")

        if "id_client" not in vendas.columns or "id_product" not in vendas.columns:
            raise DataValidationError("Colunas 'id_client' ou 'id_product' não existem no dataset.")

        matriz = vendas.groupby(["id_client", "id_product"]).size().unstack(fill_value=0)
        matriz = (matriz > 0).astype(int)

        if matriz.empty:
            raise DataValidationError("Matriz usuário-produto está vazia.")

        similaridade = cosine_similarity(matriz.T)
        sim_df = pd.DataFrame(similaridade,
                              index=matriz.columns,
                              columns=matriz.columns)

        produto_ref = 105  # ID do GPS
        if produto_ref not in sim_df.columns:
            raise DataValidationError(f"Produto {produto_ref} não encontrado na matriz.")

        ranking = sim_df[produto_ref].drop(produto_ref).sort_values(ascending=False).head(5)
        print("Top 5 produtos similares ao", produto_ref)
        print(ranking)

        ranking.to_csv("../data/csv/produtos_similares.csv", index=True)

    except FileNotFoundError as e:
        log_error(FileProcessingError(f"Arquivo não encontrado: {e}"))
        print("Erro: arquivo CSV não foi encontrado.")
    except DataValidationError as e:
        log_error(e)
        print("Erro de validação:", e)
    except Exception as e:
        log_error(e)
        print("Erro inesperado:", e)

if __name__ == "__main__":
    recomendar_produtos()
