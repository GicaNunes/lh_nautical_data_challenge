import pandas as pd

def run():
    print("=== Previsão de Demandas rodando ===")

    vendas = pd.read_csv("data/csv/vendas_2023_2024.csv")
    vendas['sale_date'] = pd.to_datetime(vendas['sale_date'], errors='coerce')

    # Série temporal de vendas diárias
    serie_vendas = vendas.groupby('sale_date')['qtd'].sum()

    # Média móvel simples (7 dias)
    serie_vendas_ma = serie_vendas.rolling(window=7).mean()

    previsao_proxima_semana = serie_vendas_ma.iloc[-1]
    print("Previsão de vendas para próxima semana:", previsao_proxima_semana)

    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("\n=== Previsão ===\n")
        f.write("Previsão de vendas gerada com média móvel.\n")


if __name__ == "__main__":
    run()
