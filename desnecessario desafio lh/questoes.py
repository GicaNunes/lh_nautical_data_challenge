import os
import pandas as pd
import matplotlib.pyplot as plt

def run():
    print("=== Questões 4, 5 e 6 ===")

    # Caminho base (raiz do projeto)
    base_path = os.path.dirname(os.path.dirname(__file__))

    # Arquivos de dados
    vendas_path = os.path.join(base_path, "data/csv/vendas_2023_2024.csv")
    clientes_path = os.path.join(base_path, "data/json/clientes_crm.json")
    produtos_path = os.path.join(base_path, "data/csv/produtos_raw.csv")

    # Leitura dos dados
    df = pd.read_csv(vendas_path)
    clientes = pd.read_json(clientes_path)
    produtos = pd.read_csv(produtos_path)

    # Ajuste de datas
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

    # ============================================================
    # Questão 4 – Distribuição ou ranking de prejuízos por produto
    # ============================================================
    # Exemplo: assumindo que existe coluna 'custo_unitario'
    if 'custo_unitario' in df.columns:
        df['prejuizo'] = df['total'] - (df['qtd'] * df['custo_unitario'])
        ranking_prejuizo = df.groupby('name')['prejuizo'].sum().sort_values()

        ranking_prejuizo.plot(kind='barh', figsize=(10,6), title="Prejuízos por Produto")
        plt.savefig(os.path.join(base_path, "visuals/prejuizos_produtos.png"))
        plt.close()

        with open(os.path.join(base_path, "resultados.txt"), "a", encoding="utf-8") as f:
            f.write("\n=== Questão 4 – Prejuízos por Produto ===\n")
            f.write("Gráfico salvo em visuals/prejuizos_produtos.png\n")
            f.write("Top produtos com maior prejuízo:\n" + str(ranking_prejuizo.head()) + "\n")
    else:
        print("Coluna 'custo_unitario' não encontrada. Ajuste necessário para calcular prejuízo.")

    # ============================================================
    # Questão 5 – Clientes com maior lucro acumulado
    # ============================================================
    lucro_clientes = df.groupby('id_client')['total'].sum().sort_values(ascending=False).head(10)
    lucro_clientes.plot(kind='bar', figsize=(10,6), title="Top Clientes por Lucro Acumulado")
    plt.savefig(os.path.join(base_path, "visuals/top_clientes_lucro.png"))
    plt.close()

    with open(os.path.join(base_path, "resultados.txt"), "a", encoding="utf-8") as f:
        f.write("\n=== Questão 5 – Clientes com maior lucro acumulado ===\n")
        f.write("Gráfico salvo em visuals/top_clientes_lucro.png\n")
        f.write("Top clientes:\n" + str(lucro_clientes) + "\n")

    # ============================================================
    # Questão 6 – Vendas médias por dia da semana
    # ============================================================
    dias = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    media_semana = df.groupby(df['sale_date'].dt.day_name())['qtd'].mean().reindex(dias, fill_value=0)

    media_semana.plot(kind='bar', figsize=(8,5), title="Vendas Médias por Dia da Semana")
    plt.savefig(os.path.join(base_path, "visuals/vendas_media_semana.png"))
    plt.close()

    with open(os.path.join(base_path, "resultados.txt"), "a", encoding="utf-8") as f:
        f.write("\n=== Questão 6 – Vendas médias por dia da semana ===\n")
        f.write("Gráfico salvo em visuals/vendas_media_semana.png\n")
        f.write(str(media_semana) + "\n")

if __name__ == "__main__":
    run()
