import pandas as pd
from errors import FileProcessingError, DataValidationError, log_error

def limpar_produtos():
    try:
        # Carregar dataset bruto
        df = pd.read_csv("../data/csv/produtos_raw.csv")

        # Padronizar colunas
        df.columns = df.columns.str.lower()

        # Contar linhas originais
        linhas_originais = df.shape[0]

        # Verificar se existe a coluna 'actual_category'
        if "actual_category" in df.columns:
            df["categoria"] = df["actual_category"].str.strip().str.lower()
            mapa_categorias = {
                "eletronicos": "eletrônicos",
                "eletrônico": "eletrônicos",
                "propulsao": "propulsão",
                "propulsor": "propulsão",
                "ancoragem": "ancoragem",
                "ancora": "ancoragem"
            }
            df["categoria"] = df["categoria"].replace(mapa_categorias)
        else:
            raise DataValidationError("A coluna 'actual_category' não existe no CSV.")

        # Converter valores para numérico (se existir coluna 'valor' ou 'price')
        if "valor" in df.columns:
            df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        elif "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # Remover duplicatas
        df_limpo = df.drop_duplicates()

        # Contar linhas após limpeza
        linhas_final = df_limpo.shape[0]
        duplicatas_removidas = linhas_originais - linhas_final

        print(f"Produtos duplicados removidos: {duplicatas_removidas}")

        # Salvar dataset limpo
        df_limpo.to_csv("../data/csv/produtos_clean.csv", index=False)
        print("Arquivo produtos_clean.csv gerado com sucesso!")

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
    limpar_produtos()
