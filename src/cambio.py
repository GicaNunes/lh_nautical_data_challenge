import pandas as pd
import requests
from datetime import datetime

# Série 1 = PTAX venda (cotação média diária do dólar)
data_inicial = "01/01/2023"
data_final = datetime.today().strftime("%d/%m/%Y")

url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    cambio = pd.DataFrame(data)

    # Renomear colunas
    cambio.rename(columns={"data": "date", "valor": "usd_brl"}, inplace=True)

    # Converter tipos
    cambio["date"] = pd.to_datetime(cambio["date"], dayfirst=True)
    cambio["usd_brl"] = pd.to_numeric(cambio["usd_brl"], errors="coerce")

    # Salvar em CSV
    cambio.to_csv("../data/csv/cambio_diario.csv", index=False)

    print("Arquivo cambio_diario.csv gerado com sucesso!")
    print(cambio.head())
else:
    print("Erro na requisição:", response.status_code)
