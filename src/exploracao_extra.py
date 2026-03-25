import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from errors import FileProcessingError, DataValidationError, log_error

def run():
    print("=== Exploração Extra rodando ===")
    try:
        vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")
        produtos = pd.read_csv("../data/csv/produtos_raw.csv")
        clientes = pd.read_json("../data/json/clientes_crm.json")

        if "sale_date" not in vendas.columns or "qtd" not in vendas.columns:
            raise DataValidationError("Colunas 'sale_date' ou 'qtd' não existem em vendas.")

        vendas['sale_date'] = pd.to_datetime(vendas['sale_date'], errors='coerce')

        # --- Sazonalidade ---
        vendas['mes'] = vendas['sale_date'].dt.to_period('M')
        mensal = vendas.groupby('mes')['qtd'].sum()
        mensal.plot(kind='line', figsize=(10,5), title="Vendas Mensais")
        plt.savefig("../visuals/vendas_mensais_extra.png")
        plt.close()

        vendas['dia_semana'] = vendas['sale_date'].dt.day_name()
        semana = vendas.groupby('dia_semana')['qtd'].sum()
        semana.plot(kind='bar', figsize=(8,5), title="Vendas por Dia da Semana")
        plt.savefig("../visuals/vendas_semana_extra.png")
        plt.close()

        # --- Segmentação de clientes ---
        df = vendas.merge(clientes, left_on='id_client', right_on='code', how='left')
        if "total" not in df.columns:
            raise DataValidationError("Coluna 'total' não existe em vendas.")
        df['ticket_medio'] = df['total'] / df['qtd']
        ticket_clientes = df.groupby('full_name')['ticket_medio'].mean().sort_values(ascending=False)
        print("Top 5 clientes VIP (ticket médio):\n", ticket_clientes.head())

        # --- Ranking de produtos ---
        df = vendas.merge(produtos, left_on='id_product', right_on='code', how='left')
        ranking = df.groupby('actual_category')['qtd'].sum().sort_values(ascending=False)
        ranking.plot(kind='bar', figsize=(10,5), title="Ranking de Categorias")
        plt.savefig("../visuals/ranking_categorias.png")
        plt.close()

        top_produtos = df.groupby('name')['qtd'].sum().sort_values(ascending=False).head(10)
        top_produtos.plot(kind='barh', figsize=(10,5), title="Top 10 Produtos")
        plt.savefig("../visuals/top_produtos.png")
        plt.close()

        # --- Co-ocorrência de produtos ---
        coocorrencia = df.groupby(['id_client','sale_date'])['name'].apply(list)
        pares = Counter()
        for lista in coocorrencia:
            for i in range(len(lista)):
                for j in range(i+1, len(lista)):
                    pares[(lista[i], lista[j])] += 1
        print("Top pares de produtos comprados juntos:\n", pares.most_common(5))

        with open("../resultados.txt", "a", encoding="utf-8") as f:
            f.write("\n=== Exploração Extra ===\n")
            f.write("Top 5 clientes VIP:\n" + str(ticket_clientes.head()) + "\n")
            f.write("Top pares de produtos comprados juntos:\n" + str(pares.most_common(5)) + "\n")

    except FileNotFoundError as e:
        log_error(FileProcessingError(f"Arquivo não encontrado: {e}"))
        print("Erro: algum arquivo CSV/JSON não foi encontrado.")
    except DataValidationError as e:
        log_error(e)
        print("Erro de validação:", e)
    except Exception as e:
        log_error(e)
        print("Erro inesperado:", e)

if __name__ == "__main__":
    run()
