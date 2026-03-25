import pandas as pd
from sklearn.metrics import mean_absolute_error
from errors import DataValidationError, FileProcessingError, log_error

def avaliar_baseline():
    try:
        vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")

        produto = vendas[vendas["id_product"] == 105].copy()
        if produto.empty:
            raise DataValidationError("Produto com ID 105 não encontrado no dataset.")

        produto["sale_date"] = pd.to_datetime(produto["sale_date"], errors="coerce")
        diario = produto.groupby("sale_date")["qtd"].sum().reset_index()

        treino = diario[diario["sale_date"] <= pd.to_datetime("2023-12-31")].copy()
        teste = diario[(diario["sale_date"] >= pd.to_datetime("2024-01-01")) &
                       (diario["sale_date"] <= pd.to_datetime("2024-01-31"))].copy()

        print("Linhas treino:", len(treino))
        print("Linhas teste:", len(teste))

        if teste.empty:
            raise DataValidationError("Não há dados de vendas para Janeiro/2024. O baseline não pode ser avaliado.")

        previsoes = []
        for data in teste["sale_date"]:
            historico = diario[diario["sale_date"] < data]
            previsao = historico["qtd"].tail(7).mean()
            previsoes.append(previsao)

        teste["previsao"] = previsoes
        mae = mean_absolute_error(teste["qtd"], teste["previsao"])
        print("MAE (Janeiro/2024):", round(mae, 2))

        teste.to_csv("../data/csv/previsao_motor_yamaha.csv", index=False)

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
    avaliar_baseline()
