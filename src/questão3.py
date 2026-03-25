import pandas as pd
import json
from errors import FileProcessingError, DataValidationError, log_error

def gerar_custos_importacao():
    try:
        # Carregar o arquivo JSON
        with open("../data/json/custos_importacao.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        linhas = []
        for produto in data:
            for preco in produto.get("prices", []):
                # Detecta automaticamente os nomes das chaves
                data_chave = preco.get("start_date") or preco.get("date") or preco.get("inicio")
                preco_chave = preco.get("usd_price") or preco.get("price") or preco.get("valor")

                if not data_chave or not preco_chave:
                    raise DataValidationError("Registro de preço sem data ou valor válido.")

                linhas.append({
                    "product_id": produto.get("product_id"),
                    "product_name": produto.get("product_name"),
                    "category": produto.get("category"),
                    "start_date": data_chave,
                    "usd_price": preco_chave
                })

        # Criar DataFrame
        df = pd.DataFrame(linhas)

        # Converter tipos
        if "start_date" in df.columns:
            df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
        if "usd_price" in df.columns:
            df["usd_price"] = pd.to_numeric(df["usd_price"], errors="coerce")

        # Remover duplicatas
        df = df.drop_duplicates()

        # Salvar em CSV
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
