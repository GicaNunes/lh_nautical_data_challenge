import pandas as pd
from errors import FileProcessingError, DataValidationError, log_error

def executar_questao1():
    try:
        # Carregar dataset
        df = pd.read_csv("../data/csv/vendas_2023_2024.csv")

        # Converter datas
        df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

        if df['sale_date'].isnull().all():
            raise DataValidationError("Coluna 'sale_date' não pôde ser convertida corretamente.")

        # Parte 1 – Visão geral
        print("Quantidade de linhas:", df.shape[0])
        print("Quantidade de colunas:", df.shape[1])
        print("Data mínima:", df['sale_date'].min())
        print("Data máxima:", df['sale_date'].max())

        # Parte 2 – Estatísticas da coluna 'total'
        print("Valor mínimo:", df['total'].min())
        print("Valor máximo:", df['total'].max())
        print("Valor médio:", df['total'].mean())

    except FileNotFoundError as e:
        log_error(FileProcessingError(f"Arquivo não encontrado: {e}"))
        print("Erro: arquivo CSV não encontrado.")
    except Exception as e:
        log_error(e)
        print("Erro inesperado:", e)

if __name__ == "__main__":
    executar_questao1()
