import pandas as pd
import json
from errors import FileProcessingError, DataValidationError, log_error

def gerar_custos_importacao():
    try:
        with open("../data/json/custos_importacao.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        linhas = []
        for produto in data:
            for preco in produto.get("historic_data", []):
                if not preco.get("start_date") or not preco.get("usd_price"):
                    raise DataValidationError("Registro sem data ou preço válido.")

                linhas.append({
                    "product_id": produto.get("product_id"),
                    "product_name": produto.get("product_name"),
                    "category": produto.get("category"),
                    "start_date": preco.get("start_date"),
                    "usd_price": preco.get("usd_price")
                })

        df = pd.DataFrame(linhas)

        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce", dayfirst=True)
        df["usd_price"] = pd.to_numeric(df["usd_price"], errors="coerce")

        df = df.drop_duplicates()

        print("Total de entradas de importação após normalização:", df.shape[0])

        df.to_csv("../data/csv/custos_importacao.csv", index=False)
        print("Arquivo custos_importacao.csv gerado com sucesso!")

    except FileNotFoundError as e:
        log_error(FileProcessingError(f"Arquivo JSON não encontrado: {e}"))
        print("Erro: arquivo JSON não foi encontrado.")
    except DataValidationError as e:
        log_error(e)
        print("Erro de validação:", e)
    except Exception as e:
        log_error(e)
        print("Erro inesperado:", e)

if __name__ == "__main__":
    gerar_custos_importacao()
